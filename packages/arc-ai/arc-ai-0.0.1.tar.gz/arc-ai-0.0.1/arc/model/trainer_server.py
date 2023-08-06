
import json
import logging
from typing import Any, Dict
from dataclasses import dataclass
import sys
from pathlib import Path
import time
import os
import shutil

from simple_parsing import ArgumentParser
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse, StreamingResponse
from starlette.schemas import SchemaGenerator
import uvicorn

from arc.data.encoding import ShapeEncoder
from arc.model.metrics import Metrics
from arc.scm import SCM
from arc.image.build import REPO_ROOT
from arc.model.types import BUILD_MNT_DIR
from arc.model.trainer import Trainer

from trainer import Trainer
from trainer import *
from arc.data.shapes.image import ImageData
from arc.data.shapes.classes import ClassData

scm = SCM()

app = Starlette(debug=True)

schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Trainer", "version": "d946d04-25f6810"}}
)

@app.route("/health")
def health(request):
    return JSONResponse({"status": "alive"})

@app.route("/info")
def info(request):
    # model_dict = model.opts().to_dict()
    return JSONResponse({"version": scm.sha(), "env-sha": scm.env_sha()})

@app.route('/train', methods=["POST"])
async def train(request):
    jdict = await request.json()
    trainer = Trainer[ImageData, ClassData]()
    res = trainer.train(**jdict)

    ret = {}
    for model_uri, report in res.items():
        ret[model_uri] = report.repr_json()

    return JSONResponse(ret)

@app.route("/schema")
def openapi_schema(request):
    return schemas.OpenAPIResponse(request=request)


if __name__ == "__main__":
    pkgs: Dict[str, str] = {}
    for fp in scm.all_files():
        dir = os.path.dirname(fp)
        pkgs[dir] = ""

    logging.info("starting server version 'd946d04-25f6810' on port: 8080")
    uvicorn.run("__main__:app", host="0.0.0.0", port=8080, log_level="debug", workers=1, reload=True, reload_dirs=pkgs.keys())
        