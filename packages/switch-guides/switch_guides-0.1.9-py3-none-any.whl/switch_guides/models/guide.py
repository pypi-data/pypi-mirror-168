# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


from typing import List, Optional, Union
from pydantic import BaseModel
from .literals import STATUS_STATE
from .step import SwitchGuideStep, SwitchGuideStepComponent, SwitchGuideStepDefinitionUiAssets, SwitchGuideStepDependency, SwitchGuideStepOverrides


class SwitchGuideStatus(BaseModel):
    state: STATUS_STATE
    percentageCompleted: int = 0


class SwitchGuideDefinitionOptions(BaseModel):
    enable_live_notification: bool = False


class SwitchGuideSummaryStepEvents(BaseModel):
    componentOnCompletion: Union[SwitchGuideStepComponent, None]


class SwitchGuideSummaryStepConfigDefinition(BaseModel):
    uiAssets: Optional[SwitchGuideStepDefinitionUiAssets]
    events: Optional[SwitchGuideSummaryStepEvents]


class SwitchGuideSummaryStepConfig(BaseModel):
    component: Optional[SwitchGuideStepComponent]
    uiAssets: Optional[SwitchGuideStepDefinitionUiAssets]

class SwitchGuideDefinition(BaseModel):
    id: str = ''
    name: str
    description: str
    instructions: str
    summaryStep: Optional[SwitchGuideSummaryStepConfigDefinition]
    steps: List[SwitchGuideStepDependency]
    options: Optional[SwitchGuideDefinitionOptions]


class SwitchGuideInstance(BaseModel):
    id: str
    status: SwitchGuideStatus
    steps: List[SwitchGuideStepOverrides]


class SwitchGuide(SwitchGuideDefinition, SwitchGuideInstance, BaseModel):
    id: str
    summaryStep: Optional[SwitchGuideSummaryStepConfig]
    steps: List[SwitchGuideStep]


class SwitchGuideSummary(BaseModel):
    id: str
    name: str
    createdOnUtc: str
    modifiedOnUtc: str
    description: str
    instructions: str
    status: SwitchGuideStatus
