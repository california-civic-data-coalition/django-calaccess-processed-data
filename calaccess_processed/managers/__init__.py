#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the managers from submodules and thread them together.
"""
from .flatfiles import (
    OCDFlatBallotMeasureContestManager,
    OCDFlatCandidacyManager,
    OCDFlatRetentionContestManager
)
from .proxies import (
    RawFilerToFilerTypeCdManager,
    ScrapedIncumbentElectionManager,
    OCDCommitteeManager,
    OCDCommitteeIdentifierManager,
    OCDCommitteeNameManager,
    OCDCommitteeTypeManager,
    OCDFilingManager,
    OCDFilingIdentifierManager,
    OCDFilingActionManager,
    OCDFilingActionSummaryAmountManager,
    OCDTransactionManager,
    OCDAssemblyDivisionManager,
    OCDSenateDivisionManager,
    OCDCaliforniaDivisionManager,
    OCDJurisdictionManager,
    OCDOrganizationManager,
    OCDMembershipManager,
    OCDPersonManager,
    OCDPostManager,
    OCDAssemblyPostManager,
    OCDExecutivePostManager,
    OCDSenatePostManager,
    OCDCandidacyQuerySet,
    OCDCandidacyManager,
    OCDCandidateContestQuerySet,
    OCDPartisanPrimaryManager,
    OCDElectionManager,
    OCDPartyManager
)
from .constraints import ConstraintsManager
from .filings import FilingsManager


__all__ = (
    "OCDFlatBallotMeasureContestManager",
    "OCDFlatCandidacyManager",
    "OCDFlatRetentionContestManager",
    "RawFilerToFilerTypeCdManager",
    "ScrapedIncumbentElectionManager",
    "OCDCommitteeManager",
    "OCDCommitteeIdentifierManager",
    "OCDCommitteeNameManager",
    "OCDCommitteeTypeManager",
    "OCDFilingManager",
    "OCDFilingIdentifierManager",
    "OCDFilingActionManager",
    "OCDFilingActionSummaryAmountManager",
    "OCDTransactionManager",
    "OCDAssemblyDivisionManager",
    "OCDSenateDivisionManager",
    "OCDCaliforniaDivisionManager",
    "OCDJurisdictionManager",
    "OCDOrganizationManager",
    "OCDMembershipManager",
    "OCDPersonManager",
    "OCDPostManager",
    "OCDAssemblyPostManager",
    "OCDExecutivePostManager",
    "OCDSenatePostManager",
    "OCDCandidacyQuerySet",
    "OCDCandidacyManager",
    "OCDCandidateContestQuerySet",
    "OCDPartisanPrimaryManager",
    "OCDElectionManager",
    "OCDPartyManager",
    'ConstraintsManager',
    'FilingsManager'
)
