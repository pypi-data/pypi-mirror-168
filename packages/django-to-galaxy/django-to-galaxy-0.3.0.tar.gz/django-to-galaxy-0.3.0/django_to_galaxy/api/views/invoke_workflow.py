from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.status import HTTP_404_NOT_FOUND

from django_to_galaxy.models import History, Workflow
from django_to_galaxy.api.serializers.invoke_workflow import InvokeWorkflowSerializer


class InvokeWorkflowView(GenericAPIView):
    serializer_class = InvokeWorkflowSerializer

    @swagger_auto_schema(
        operation_description="Invoke workflow using data from a history.",
        operation_summary="Invoke workflow using data from a history.",
        tags=["workflows"],
    )
    def post(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        # Retrieve history
        try:
            history = History.objects.get(id=data["history_id"])
        except ObjectDoesNotExist:
            return Response(
                {
                    "message": (
                        "Galaxy history with id ",
                        f"<{data['history_id']}> not found!",
                    )
                },
                status=HTTP_404_NOT_FOUND,
            )
        # Retrieve workflow
        try:
            workflow = Workflow.objects.get(id=data["workflow_id"])
        except ObjectDoesNotExist:
            return Response(
                {
                    "message": (
                        "Galaxy workflow with id ",
                        f"<{data['history_id']}> not found!",
                    )
                },
                status=HTTP_404_NOT_FOUND,
            )
        inv = workflow.invoke(data["datamap"], history=history)
        data["message"] = "Workflow successfully invoked."
        data["invocation_id"] = inv.id
        return Response(data=data)


class GetWorkflowDatamapTemplateView(RetrieveAPIView):
    queryset = Workflow.objects.all()

    @swagger_auto_schema(
        operation_description="Get workflow datamap to prepare workflow invocation.",
        operation_summary="Get workflow datamap to prepare workflow invocation.",
        tags=["workflows"],
    )
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        inputs = instance.galaxy_workflow.inputs
        input_mapping = {}
        datamap_template = {}
        for input_id, input_dict in inputs.items():
            input_mapping[input_id] = input_dict["label"]
            datamap_template[input_id] = {"id": "", "src": "hda"}
        return Response(
            data={"input_mapping": input_mapping, "datamap_template": datamap_template}
        )
