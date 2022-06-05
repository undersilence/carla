// Copyright (c) 2017 Computer Vision Center (CVC) at the Universitat Autonoma de Barcelona (UAB). This work is licensed under the terms of the MIT license. For a copy, see <https://opensource.org/licenses/MIT>.

#pragma once

#include "Carla/Sensor/ShaderBasedSensor.h"
#include "Carla/Actor/ActorDefinition.h"
#include "GbufferCamera.generated.h"

/**
 * Gbuffer Camera Class, for normal, AO...
 */

UCLASS()
class CARLA_API AGbufferCamera : public AShaderBasedSensor
{

	GENERATED_BODY()

public:
	static FActorDefinition GetSensorDefinition();	
	AGbufferCamera(const FObjectInitializer& ObjectInitializer);

protected:
	void PostPhysTick(UWorld* World, ELevelTick TickType, float DeltaTime) override;

};
