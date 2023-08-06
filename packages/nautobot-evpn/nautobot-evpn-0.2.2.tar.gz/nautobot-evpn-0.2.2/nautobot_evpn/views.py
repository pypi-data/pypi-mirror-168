import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.edit import CreateView
from django_tables2 import Column

from nautobot.dcim.choices import InterfaceTypeChoices
from nautobot.dcim.tables import InterfaceTable
from nautobot.ipam.models import VLAN, VRF
from nautobot.core.views.generic import BulkImportView, ObjectListView, ObjectEditView, ObjectView

from . import tables
from .forms import (
    VLANAddToVRFForm, VLANAnycastIPForm, VRFPrimaryVLANForm, JoinEthernetSegmentForm,
    EthernetSegmentForm, EthernetSegmentCSVForm,
    EthernetSegmentMembershipCSVForm
)
from .models import (
    AnycastIP, AnycastDummyIP, VRFPrimaryVLAN, VLANVRFList, EthernetSegment, EthernetSegmentMembership, Interface
)
from .utilities import redirect_to_referer

logger = logging.getLogger('nautobot.evpn')


@method_decorator(login_required, name='dispatch')
class VRFDisconnectPrimaryVLANView(View):
    def get(self, request, pk=None):
        """
        This view disconnects a VRF from a VLAN.
        """
        vlanvrf = get_object_or_404(VRFPrimaryVLAN, vrf_id=pk)
        vlanvrf.delete()
        messages.info(request, "Deleted VLAN-VRF connection.")
        return redirect_to_referer(request)


class CreateWithReturnView(CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_url'] = self.get_success_url()
        return context


class VRFPrimaryVLANView(PermissionRequiredMixin, CreateWithReturnView):
    model = VRFPrimaryVLAN
    form_class = VRFPrimaryVLANForm
    permission_required = 'ipam.change_vrf'

    def get_success_url(self):
        pk = self.request.resolver_match.kwargs['pk']
        return reverse('ipam:vrf', kwargs={'pk': pk})

    def get_initial(self):
        vrf = VRF.objects.get(pk=self.request.resolver_match.kwargs['pk'])
        return {'vrf': vrf}


@method_decorator(login_required, name='dispatch')
class RemoveVRFView(View):
    def get(self, request, pk=None):
        """
        This view disconnects a VRF from a VLAN.
        """
        vlanvrf = get_object_or_404(VLANVRFList, vlan_id=pk)
        vlanvrf.delete()
        messages.info(request, "Deleted VLAN-VRF connection.")
        return redirect_to_referer(request)


class AddVRFView(PermissionRequiredMixin, CreateWithReturnView):
    model = VLANVRFList
    form_class = VLANAddToVRFForm
    permission_required = 'ipam.change_vlan'

    def get_success_url(self):
        pk = self.request.resolver_match.kwargs['pk']
        return reverse('ipam:vlan', kwargs={'pk': pk})

    def get_initial(self):
        vlan = VLAN.objects.get(pk=self.request.resolver_match.kwargs['pk'])
        return {'vlan': vlan}


class VLANAnycastIPView(PermissionRequiredMixin, CreateWithReturnView):
    model = AnycastIP
    form_class = VLANAnycastIPForm
    permission_required = 'ipam.change_vlan'

    def get_success_url(self):
        pk = self.request.resolver_match.kwargs['pk']
        return reverse('ipam:vlan', kwargs={'pk': pk})

    def get_initial(self):
        vlan = VLAN.objects.get(pk=self.request.resolver_match.kwargs['pk'])
        ips = AnycastIP.objects.filter(vlan=vlan).values_list('ip', flat=True)
        dummy_ips = AnycastDummyIP.objects.filter(vlan=vlan).values_list('ip', flat=True)
        return {'vlan': vlan, 'ips': ips, 'dummy_ips': dummy_ips}


class JoinEthernetSegmentView(PermissionRequiredMixin, CreateWithReturnView):
    model = EthernetSegmentMembership
    form_class = JoinEthernetSegmentForm
    permission_required = 'dcim.change_interface'

    def get_success_url(self):
        pk = self.request.resolver_match.kwargs['pk']
        return reverse('dcim:interface', kwargs={'pk': pk})

    def get_initial(self):
        interface = Interface.objects.get(pk=self.request.resolver_match.kwargs['pk'])
        return {'interface': interface}


@method_decorator(login_required, name='dispatch')
class LeaveEthernetSegmentView(View):
    def get(self, request, pk=None):
        """
        This view removes an Interface from an Ethernet Segment
        """
        es_membership = get_object_or_404(EthernetSegmentMembership, pk=pk)
        es_membership.delete()
        messages.info(request, "Left Ethernet Segment")
        return redirect_to_referer(request)


class EthernetSegmentListView(PermissionRequiredMixin, ObjectListView):
    permission_required = 'dcim.view_ethernet_segment'
    queryset = EthernetSegment.objects.all()
    table = tables.EthernetSegmentTable
    action_buttons = ()
    template_name = "nautobot_evpn/ethernetsegment_list.html"


class ExtendedInterfaceTable(InterfaceTable):

    class Meta(InterfaceTable.Meta):
        pass

    def __init__(self, physical_interfaces, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.physical_interfaces = list(physical_interfaces)
        self.columns.show("underlaying_interface_type")

    underlaying_interface_type = Column(
        "Underlaying Interface Type",
        empty_values=()
    )

    def render_underlaying_interface_type(self, value, record):
        print(value, record)
        physical_interface = next(filter(lambda p: p.lag == record, self.physical_interfaces), None)
        if not physical_interface:
            return None

        c = InterfaceTypeChoices.as_dict().get(physical_interface.type)
        return c if physical_interface else None



class EthernetSegmentView(ObjectView):
    queryset = EthernetSegment.objects.all()

    def get_extra_context(self, request, instance):
        attached_interfaces = Interface.objects.filter(ethernetsegmentmembership__segment=instance).restrict(
            request.user, "view")

        physical_interfaces = Interface.objects.filter(lag__in=attached_interfaces)

        attached_interfaces_table = ExtendedInterfaceTable(
            physical_interfaces,
            attached_interfaces,
            orderable=False,
        )
        attached_interfaces_table.columns.show("untagged_vlan")
        attached_interfaces_table.columns.show("tagged_vlans")

        return {
            "attached_interfaces_table": attached_interfaces_table,
        }


class EthernetSegmentAddView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'dcim.add_ethernet_segment'
    model_form = EthernetSegmentForm
    queryset = EthernetSegment.objects.all()
    default_return_url = 'plugins:nautobot_evpn:es-list'


class EthernetSegmentImportView(BulkImportView):
    queryset = EthernetSegment.objects.all()
    model_form = EthernetSegmentCSVForm
    table = tables.EthernetSegmentTable


class EthernetSegmentMembershipImportView(BulkImportView):
    queryset = EthernetSegmentMembership.objects.all()
    model_form = EthernetSegmentMembershipCSVForm
    table = tables.EthernetSegmentMembershipTable


@method_decorator(login_required, name='dispatch')
class EthernetSegmentDeleteView(View):
    def get(self, request, pk=None):
        """
        This view deletes an Ethernet Segment
        """
        segment = get_object_or_404(EthernetSegment, pk=pk)
        segment.delete()
        return redirect_to_referer(request)
