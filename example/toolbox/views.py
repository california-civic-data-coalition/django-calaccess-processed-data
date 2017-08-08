from django.db import ProgrammingError
from django.shortcuts import render
from collections import defaultdict
from calaccess_processed.models import (
    OCDElectionProxy,
    OCDCandidacyProxy,
    OCDPostProxy,
    OCDPersonProxy,
    OCDPartyProxy
)
from opencivicdata.elections.models import CandidateContest
from django.views.generic import DetailView, ListView



def election_list(request):
    object_list = OCDElectionProxy.objects.all()
    group_dict = defaultdict()
    for obj in object_list:
        group_dict.setdefault(obj.date.year, []).append(obj)
    group_list = sorted(group_dict.items(), key=lambda x:x[0], reverse=True)
    context = dict(object_list=object_list, group_list=group_list)
    template = "election_list.html"
    return render(request, template, context)


def election_detail(request, id):
    obj = OCDElectionProxy.objects.get(id=id)
    context = dict(object=obj)
    template = "election_detail.html"
    return render(request, template, context)


def candidatecontest_detail(request, id):
    obj = CandidateContest.objects.get(id=id)
    candidate_list = OCDCandidacyProxy.objects.filter(contest=obj)
    context = dict(object=obj, candidate_list=candidate_list)
    template = "candidatecontest_detail.html"
    return render(request, template, context)


class PostDetail(DetailView):
    model = OCDPostProxy
    template_name = "post_detail.html"


class PersonDetail(DetailView):
    model = OCDPersonProxy
    template_name = "person_detail.html"


class PartyList(ListView):
    model = OCDPartyProxy
    template_name = "party_list.html"


class PartyDetail(DetailView):
    model = OCDPartyProxy
    template_name = "party_detail.html"


class CandidateNoPartyList(ListView):
    """
    Lists all the OCD candidates with an unknown party.
    """
    template_name = "candidatenoparty_list.html"

    def get_queryset(self):
        try:
            return OCDCandidacyProxy.objects.filter(party=OCDPartyProxy.objects.unknown())
        except (OCDPartyProxy.DoesNotExist, ProgrammingError):
            return OCDCandidacyProxy.objects.none()


class PrimaryNoPartyList(ListView):
    """
    Lists all the OCD partisan primaries with an unknown party.
    """
    template_name = "electionnoparty_list.html"

    def get_queryset(self):
        primary_list = OCDElectionProxy.partisan_primaries.all()
        contest_list = CandidateContest.objects.filter(election__in=primary_list)
        try:
            return contest_list.filter(party=OCDPartyProxy.objects.unknown())
        except OCDPartyProxy.DoesNotExist:
            return CandidateContest.objects.none()
