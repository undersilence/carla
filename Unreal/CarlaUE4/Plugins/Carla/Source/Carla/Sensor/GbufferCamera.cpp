// Copyright (c) 2017 Computer Vision Center (CVC) at the Universitat Autonoma de Barcelona (UAB). This work is licensed under the terms of the MIT license. For a copy, see <https://opensource.org/licenses/MIT>.

#include "Carla.h"
#include "Carla/Sensor/PixelReader.h"
#include "Carla/Sensor/GbufferCamera.h"
#include "Carla/Actor/ActorBlueprintFunctionLibrary.h"

FActorDefinition AGbufferCamera::GetSensorDefinition()
{
  return UActorBlueprintFunctionLibrary::MakeCameraDefinition(TEXT("gbuffer"));
}

AGbufferCamera::AGbufferCamera(const FObjectInitializer& ObjectInitializer) : Super(ObjectInitializer)
{
  AddPostProcessingMaterial(
    TEXT("Material'/Carla/PostProcessingMaterials/PhysicLensDistortion.PhysicLensDistortion'"));
  AddPostProcessingMaterial(
    TEXT("Material'/Carla/PostProcessingMaterials/NormalMaterial.NormalMaterial'"));
} 

void AGbufferCamera::PostPhysTick(UWorld* World, ELevelTick TickType, float DeltaTime)
{
  TRACE_CPUPROFILER_EVENT_SCOPE(AGbufferCamera::PostPhysTick);
  FPixelReader::SendPixelsInRenderThread(*this);
}
