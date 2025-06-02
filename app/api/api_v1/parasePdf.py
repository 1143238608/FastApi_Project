# -*- coding: utf-8 -*-
"""
    @Time   : 2025/6/1 10:55
    @Author : mxy
"""
import os

from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
from magic_pdf.data.dataset import PymuDocDataset
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze
from magic_pdf.config.enums import SupportedPdfParseMethod
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PdfRequest(BaseModel):
    file_path: str

# @router.api_route("/parsePdf/",methods=["GET"])
async def parse_PDF(file_path:str):
    # args
    __dir__ = os.path.dirname(os.path.abspath(__file__))
    pdf_file_name = os.path.join(__dir__, "pdfs", file_path)  # replace with the real pdf path
    name_without_extension = os.path.basename(pdf_file_name).split('.')[0]
    print(name_without_extension)

    # prepare env
    local_image_dir = os.path.join(__dir__, "output", name_without_extension, "images")
    local_md_dir = os.path.join(__dir__, "output", name_without_extension)
    image_dir = str(os.path.basename(local_image_dir))
    os.makedirs(local_image_dir, exist_ok=True)

    # 初始化两个  FileBasedDataWriter  对象，分别用于写入图像和Markdown文件
    image_writer, md_writer = FileBasedDataWriter(local_image_dir), FileBasedDataWriter(local_md_dir)

    # 使用  FileBasedDataReader  读取PDF文件的内容，将其存储为字节数据
    reader1 = FileBasedDataReader("")
    pdf_bytes = reader1.read(pdf_file_name)  # read the pdf content

    # 将PDF文件的内容传递给  PymuDocDataset  ，用于后续处理
    ## Create Dataset Instance
    ds = PymuDocDataset(pdf_bytes)

    ## 调用  classify()  方法判断PDF文件是否需要OCR处理
    if ds.classify() == SupportedPdfParseMethod.OCR:
        infer_result = ds.apply(doc_analyze, ocr=True)

        ## pipeline
        pipe_result = infer_result.pipe_ocr_mode(image_writer)

    else:
        infer_result = ds.apply(doc_analyze, ocr=False)

        ## pipeline
        pipe_result = infer_result.pipe_txt_mode(image_writer)

    ### 获取模型推理结果
    model_inference_result = infer_result.get_infer_res()
    print("model_inference_result=======>",model_inference_result)

    ###  将布局和文本跨度结果绘制到PDF文件中
    pipe_result.draw_layout(os.path.join(local_md_dir, f"{name_without_extension}_layout.pdf"))

    pipe_result.draw_span(os.path.join(local_md_dir, f"{name_without_extension}_spans.pdf"))

    ### 生成Markdown内容，并将其保存到Markdown文件中
    md_content = pipe_result.get_markdown(image_dir)
    print("md_content=======>"+md_content)

    pipe_result.dump_md(md_writer, f"{name_without_extension}.md", image_dir)

    ### 生成内容列表，并将其保存为JSON文件
    content_list_content = pipe_result.get_content_list(image_dir)

    ### dump content list
    pipe_result.dump_content_list(md_writer, f"{name_without_extension}_content_list.json", image_dir)

    ### 生成内容列表，并将其保存为JSON文件
    middle_json_content = pipe_result.get_middle_json()

    ### 生成中间JSON数据，并将其保存为JSON文件
    pipe_result.dump_middle_json(md_writer, f'{name_without_extension}_middle.json')

    return md_content

@router.get("/parsePdf/")
async def parse_pdf_get(file_path: str):
    return await parse_PDF(file_path)

@router.post("/parsePdf/")
async def parse_pdf_post(request: PdfRequest):
    return await parse_PDF(request.file_path)