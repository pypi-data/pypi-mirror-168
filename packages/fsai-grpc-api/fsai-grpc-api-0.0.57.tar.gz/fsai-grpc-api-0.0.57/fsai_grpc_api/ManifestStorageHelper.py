import grpc
import json, jsonlines
from beartype.typing import Generator
from loguru import logger
from google.protobuf.timestamp_pb2 import Timestamp
from fsai_grpc_api.protos import category_api_pb2, category_api_pb2_grpc
from fsai_grpc_api.protos import detection_api_pb2, detection_api_pb2_grpc
from fsai_grpc_api.protos import (
    detection_instance_api_pb2,
    detection_instance_api_pb2_grpc,
)
from fsai_grpc_api.protos import feature_api_pb2, feature_api_pb2_grpc
from fsai_grpc_api.protos import image_api_pb2, image_api_pb2_grpc
from fsai_grpc_api.protos import source_api_pb2, source_api_pb2_grpc
from fsai_grpc_api.protos import query_api_pb2, query_api_pb2_grpc
from fsai_grpc_api.protos import workflow_api_pb2, workflow_api_pb2_grpc
from google.protobuf.json_format import MessageToDict
from pydash import get
from beartype import beartype


@beartype
def get_manifest_reader(fsai_manifest_path: str):
    # Open the fsai_manifest_path
    with jsonlines.open(fsai_manifest_path) as reader:

        # Read the next line in the file
        for line in reader.iter(type=dict, skip_invalid=True):

            # Return the line
            yield line


@beartype
def get_api_clients(server: str = "localhost:8080") -> dict:
    # Connect to the gRPC channel
    channel = grpc.insecure_channel(server)

    # Create a stub (client)
    return {
        "category": category_api_pb2_grpc.CategoryApiStub(channel),
        "feature": feature_api_pb2_grpc.FeatureApiStub(channel),
        "detection": detection_api_pb2_grpc.DetectionApiStub(channel),
        "detection_instance": detection_instance_api_pb2_grpc.DetectionInstanceApiStub(
            channel
        ),
        "image": image_api_pb2_grpc.ImageApiStub(channel),
        "source": source_api_pb2_grpc.SourceApiStub(channel),
        "query": query_api_pb2_grpc.QueryApiStub(channel),
        "workflow": workflow_api_pb2_grpc.WorkflowApiStub(channel),
    }


class ManifestStorageHelper:
    @beartype
    def __init__(
        self,
        grpc_clients,
        manifest_reader: Generator,
    ) -> None:
        self.grpc_clients = grpc_clients
        self.manifest_reader = manifest_reader

    @beartype
    def get_height(self, detection: dict) -> float:
        height = get(detection, "inferred.adjusted_height", 0)

        if height == None:
            return float(0)

        return float(height)

    @beartype
    def get_lat_lon(self, detection: dict) -> tuple[float, float]:
        lat = get(detection, "inferred.best_lat")
        lon = get(detection, "inferred.best_lon")
        return lat, lon

    @beartype
    def get_timestamp(self) -> Timestamp:
        # Get the current timestamp as protobuf
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        return timestamp

    @beartype
    def find_or_create_workflow(self, line: dict) -> tuple[int, int]:
        # Create the workflow request
        req = workflow_api_pb2.WorkflowRequest(
            name=get(line, "workflow.name"),
        )

        # Find or create the workflow
        workflow = self.grpc_clients["workflow"].FindOrCreateWorkflow(req)

        # Get the workflow id from the database
        workflow_id = get(workflow, "id")

        # Get the workflow part id from the lineect
        part_id = get(line, "workflow.part_id")

        return workflow_id, part_id

    @beartype
    def find_or_create_image(self, line: dict) -> int:
        # Create the image request
        req = image_api_pb2.ImageRequest(
            name=get(line, "image.name"),
            width=get(line, "image.width"),
            height=get(line, "image.height"),
        )
        # Find or create the image
        image = self.grpc_clients["image"].FindOrCreateImage(req)

        # Return the image id
        return image.id

    @beartype
    def find_or_create_feature(self, line: dict) -> int:

        feature = get(line, "feature", {})

        # Create the feature request
        req = feature_api_pb2.FeatureRequest(
            vendor_name="maxar",
            vendor_id=get(feature, "feature_id", ""),
            feature=json.dumps(feature),
        )

        # Find or create the feature
        feature = self.grpc_clients["feature"].FindOrCreateFeature(req)

        return feature.id

    @beartype
    def find_or_create_category(self, detection: dict) -> int:

        # Setup the category request
        req = category_api_pb2.CategoryRequest(
            name=get(detection, "category.name"),
        )
        category = self.grpc_clients["category"].FindOrCreateCategory(req)

        return category.id

    @beartype
    def find_or_create_detection(
        self,
        lat: float,
        lon: float,
        category_id: int,
    ) -> int:
        # Setup the detection source request
        req = detection_api_pb2.DetectionRequest(
            lat=lat,
            lon=lon,
            category_id=category_id,
        )
        detection = self.grpc_clients["detection"].FindOrCreateDetection(req)

        logger.info("Insert Detection: {}".format(MessageToDict(detection)))

        return detection.id

    @beartype
    def find_or_create_detection_instance(
        self,
        workflow_id: int,
        part_id: int,
        image_id: int,
        detection_id: int,
        feature_id: int,
        source_id: int,
        score: float,
        height: float,
        height_inferred: bool,
        detected_at: Timestamp,
    ) -> int:
        # Setup the detection instance request
        req = detection_instance_api_pb2.DetectionInstanceRequest(
            workflow_id=workflow_id,
            part_id=part_id,
            image_id=image_id,
            detection_id=detection_id,
            feature_id=feature_id,
            source_id=source_id,
            score=score,
            height=height,
            height_inferred=height_inferred,
            detected_at=detected_at,
        )
        detection_instance = self.grpc_clients[
            "detection_instance"
        ].FindOrCreateDetectionInstance(req)

        logger.info(
            "Insert Detection Instance: {}".format(MessageToDict(detection_instance))
        )

        return detection_instance.id

    @beartype
    def find_or_create_source(self, name: str) -> int:
        # Setup the detection source request
        req = source_api_pb2.SourceRequest(name=name)

        source = self.grpc_clients["source"].FindOrCreateSource(req)

        logger.info("Insert Detection Source: {}".format(MessageToDict(source)))

        return source.id

    @beartype
    def process(self, source_name: str) -> None:

        source_id = self.find_or_create_source(
            name=source_name,
        )

        for line in self.manifest_reader:

            feature_id = self.find_or_create_feature(line)

            workflow_id, part_id = self.find_or_create_workflow(line)

            image_id = self.find_or_create_image(line)

            for detection in line["detections"]:

                lat, lon = self.get_lat_lon(detection)

                height = self.get_height(detection)

                height_inferred = False if height == 0 else True

                timestamp = self.get_timestamp()

                ##############################
                # Find or create data via api
                ##############################
                category_id = self.find_or_create_category(detection)

                detection_id = self.find_or_create_detection(
                    lat=lat, lon=lon, category_id=category_id
                )

                # Setup the detection instance request
                detection_instance_id = self.find_or_create_detection_instance(
                    workflow_id=workflow_id,
                    part_id=part_id,
                    image_id=image_id,
                    detection_id=detection_id,
                    feature_id=feature_id,
                    source_id=source_id,
                    score=detection["score"],
                    height=height,
                    height_inferred=height_inferred,
                    detected_at=timestamp,
                )
                logger.info(detection_instance_id)
