# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


from typing import List, Optional, Union
import uuid
from pydantic import BaseModel
from .guide import SwitchGuide, SwitchGuideDefinition, SwitchGuideInstance
from .step import SwitchGuideStepComponent, SwitchGuideStepDefinition, SwitchGuideStepDefinitionUiAssets, SwitchGuideStepData, SwitchGuideStepStatus


class SwitchGuideExecuteApiInput(BaseModel):
    journeyInstanceId: str
    journeyInstance: SwitchGuideInstance = None
    journeyDefinition: SwitchGuideDefinition = None
    journeyStepDefinitions: List[SwitchGuideStepDefinition] = []
    stepId: str = ''
    data: dict = ''


class SwitchGuideStepApiResponse(BaseModel):
    data: dict = None
    errorMessage: str = ''
    status: SwitchGuideStepStatus = None
    uiAssets: SwitchGuideStepDefinitionUiAssets = None
    component: Union[SwitchGuideStepComponent, None] = None


class SwitchGuideApiResponse(BaseModel):
    success: bool = True
    errorMessage: str = ''
    journey: SwitchGuide = None
    journeyInstance: SwitchGuideInstance = None


class SwitchGuideFetchApiInput(BaseModel):
    journeyInstance: SwitchGuideInstance = None
    journeyDefinition: SwitchGuideDefinition = None
    journeyStepDefinitions: List[SwitchGuideStepDefinition] = []


class SwitchGuideFetchApiResponse(BaseModel):
    success: bool = True
    errorMessage: str = ''
    journey: SwitchGuide = None
    journeyInstance: SwitchGuideInstance = None


class SwitchGuideStepProcessInput(BaseModel):
    journey_id: uuid.UUID
    stepData: Optional[SwitchGuideStepData] = {}
