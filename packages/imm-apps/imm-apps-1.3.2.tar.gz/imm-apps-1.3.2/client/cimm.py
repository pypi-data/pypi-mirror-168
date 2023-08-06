# import context
from datetime import date
from api.login import get_session
import json
from api.routers.case import permission_check
from source.excel import Excel
from pathlib import Path
import typer, json
from utils.utils import append_ext, remove_ext
from system.models import get_models
from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.style import Style
from termcolor import colored
from basemodels.wordmaker import WordMaker
from system.config import Default
from utils.utils import makeTable
from basemodels.experience.employmentcert import ExperienceModel

# Get project's home directory,
BASEDIR = Path(__file__).parents[1]
# All data directory
DATADIR = BASEDIR / "data"
URL = "http://127.0.0.1:8000/"

app = typer.Typer()
console = Console()


session = get_session()

headers = {"accept": "application/json", "Content-Type": "application/json"}
error_style = Style(color="red")
success_style = Style(color="green")


def getJsonData(excel_file_name):
    e = Excel(excel_name=excel_file_name)
    return json.loads(e.json)


def show_exception(e: Exception):
    console.print(e, style="red")


def show_error(e):
    console.print(e, style="red")


def show_warning(msg: str):
    console.print(msg, style="yellow")


def print_errors(r):
    if r.status_code == 401:
        print(r.json().get("detail"))
    elif r.status_code == 422:
        console.print("Validation erro:", style=error_style)
        print(r.json()["detail"])


def getModel(model_name: str):
    # get model, and its instance
    models = get_models(rcic_company_id_name="", temp_num=1)
    model = models.get(model_name)
    if not model:
        show_error(f"{model_name} is not a valid model name.")
        exit(1)
    class_list = model["class_list"]
    the_class = __import__(model["path"], fromlist=class_list)
    the_model = getattr(the_class, class_list[1])  # No 2 is the Excel model
    return the_model


@app.command()
def man(model: str = typer.Argument(None, help="A model name, such as 5708")):
    """Manual of imm app"""
    models = get_models(rcic_company_id_name="", temp_num=1)
    # give specific manu for a model
    if model:
        if model not in models:
            show_error(
                f"{model} is not valid in defined models. Please use 'imm man' to check all models"
            )
            return
        help = models.get(model).get("help")
        if help:
            # print(f"{help.get('description')}")
            # print(tabulate(help.get("helps"), tablefmt="fancy_grid"))
            table = makeTable(f"Help for model {model}", help.get("helps"))
            console.print(table)

        else:
            print("There is no help info provided yet.")
    else:

        table = Table(title="Models List")
        table.add_column("Model", justify="left", style="cyan", no_wrap=True)
        table.add_column("Word", style="magenta")
        table.add_column("Pdf Form", style="magenta")
        table.add_column("Web Form ", style="magenta")
        table.add_column("Description", justify="left", style="green")

        contents = []
        for model, value in models.items():
            word_template = value.get("docx_template")
            pdf_function = value.get("pdf_function")
            web_function = value.get("web_function")
            if word_template:
                temp_name = ", ".join(word_template)
            else:
                temp_name = ""
            contents.append(
                [
                    model,
                    Path(temp_name).name,
                    pdf_function,
                    web_function,
                    value["remark"],
                ]
            )
        print(
            "Every model can do two things. 1. -m make excel document 2. -c check excel content based on the model\nFor specific help, enter mmc model_name to get the model's details.",
        )
        for content in contents:
            table.add_row(*content)

        console.print(table)


@app.command()
def make(model: str, output_excel_name: str):
    """Make excel based on model"""
    output_excel_name = append_ext(output_excel_name, ".xlsx")
    file_exists = Path(output_excel_name).exists()
    if file_exists:
        overwrite = typer.confirm(f"{output_excel_name} is existed, overwrite?")
        if not overwrite:
            return
    # create excel
    request = {
        "model": model,
    }
    r = session.post(URL + "case/make", json=request, headers=headers)
    if r.status_code == 401:
        print(r.json().get("detail"))
        return

    with open(output_excel_name, "wb") as f:
        f.write(r.content)
    print(colored(f"{output_excel_name} has been created", "green"))


@app.command()
def check(model: str, excel_name: str, print_json: bool = False):
    """Check input excel based on model"""
    excel_name = append_ext(excel_name, ".xlsx")
    request = {
        "model": model,
        "data": getJsonData(excel_name),
    }
    r = session.post(URL + "case/check", json=request, headers=headers)

    if r.status_code == 200:
        print(r.json()["success"])
    else:
        print_errors(r)


@app.command()
def run(model: str, excel_name: str):
    """Run app only"""
    excel_name = append_ext(excel_name, ".xlsx")
    request = {
        "model": model,
        "data": getJsonData(excel_name),
    }
    r = session.post(URL + "case/run", json=request)

    if r.status_code == 200:
        print(r.json()["success"])
    else:
        print_errors(r)


@app.command()
def word(
    model: str,
    excel_name: str,
    word_name: str = typer.Argument(
        None,
        help="Output word name. If none, willl use excel's name without ext, plus .docx",
    ),
    doctype: str = typer.Argument(
        None,
        help="Which document to generate, such as sl, ert,eet,... Use 'imm man' to check word column for details",
    ),
    rciccompany: str = typer.Option(
        "noah", help="Rcic company short name defined in docx templates"
    ),
    tempnum: int = typer.Option(1, help="template number"),
):
    """Make word based on model and input excel"""
    # check
    excel_name = append_ext(excel_name, ".xlsx")
    if word_name:
        word_name = append_ext(word_name, ".docx")
    else:
        word_name = remove_ext(excel_name) + ".docx"

    word_file_exists = Path(word_name).exists()
    excel_file_exists = Path(excel_name).exists()

    if not excel_file_exists:
        print(colored(f"{excel_name} is not existed."))
        return

    if word_file_exists:
        overwrite = typer.confirm(f"{word_name} is existed, overwrite?")
        if not overwrite:
            return

    models = get_models(rcic_company_id_name=rciccompany, temp_num=tempnum)
    template_docx_dict = models.get(model).get("docx_template")
    if not template_docx_dict:
        print(
            colored(
                f"There is no template existing in model {model.get('class_list')[0]}",
                "red",
            )
        )
        return

    request = {
        "model": model,
        "data": getJsonData(excel_name),
        "output_name": word_name,
        "doctype": doctype,
        "rciccompany": rciccompany,
        "tempnum": tempnum,
    }
    r = session.post(URL + "case/word", json=request)

    if r.status_code == 200:
        with open(word_name, "wb") as f:
            f.write(r.content)
        console.print(f"{word_name} has been downloaded from web", style=success_style)
    else:
        print_errors(r)


@app.command()
def webform(
    model: str,
    excel_name: str,
    outputjson: str = typer.Argument(
        None,
        help="Output json file name. Without input, excel's name will be used  by adding '.json'",
    ),
    rcic: str = typer.Option(Default.rcic, help="RCIC's short name"),
    initial: bool = typer.Option(
        True, help="Is this for starting a new case. Only used for BCPNP webform."
    ),
    previous: bool = typer.Option(
        False, help="Does this client have previous BCPNP application?"
    ),
    uploaddir: str = typer.Option(
        ".", help="A directory in which all files will be uploaded."
    ),
):
    """Make json file based on model and input excel for webform filling"""
    excel_name = append_ext(excel_name, ".xlsx")
    if outputjson:
        outputjson = append_ext(outputjson, ".json")
    else:
        outputjson = remove_ext(excel_name) + ".json"
    if not uploaddir:
        show_warning(
            "You did not input uploading directory. Without it , the files in current folder will be uploaded."
        )

    request = {
        "model": model,
        "data": getJsonData(excel_name),
        "output_name": outputjson,
        "rcic": rcic,
        "upload_dir": uploaddir,
    }
    r = session.post(URL + "case/webform", json=request)

    if r.status_code == 200:
        with open(outputjson, "wb") as f:
            f.write(r.content)
        console.print(f"{outputjson} has been downloaded from web", style=success_style)
    else:
        print_errors(r)


@app.command()
def pdfform(
    model: str,
    excel_name: str,
    outputjson: str = typer.Argument(
        None,
        help="Output json file name. Without input, excel's name will be used  by adding '.json'",
    ),
    rcic: str = typer.Option(Default.rcic, help="RCIC's short name"),
):
    """Make json file based on model and input excel for pdf form filling"""

    excel_name = append_ext(excel_name, ".xlsx")

    if outputjson:
        outputjson = append_ext(outputjson, ".json")
    else:
        outputjson = remove_ext(excel_name) + ".json"

    request = {
        "model": model,
        "data": getJsonData(excel_name),
        "output_name": outputjson,
        "rcic": rcic,
    }
    r = session.post(URL + "case/pdfform", json=request)

    if r.status_code == 200:
        with open(outputjson, "wb") as f:
            f.write(r.content)
        console.print(f"{outputjson} has been downloaded from web", style=success_style)
    else:
        print_errors(r)

@app.command()
def ec(
    excel_name:str,
    word_name: str = typer.Argument(
        None,
        help="Output word name. If none, willl use excel's name without ext, plus .docx",
    ),
    ):
    """Make Employment Certificate word based on input excel"""
    # check
    excel_name = append_ext(excel_name, ".xlsx")
    if word_name:
        word_name = append_ext(word_name, ".docx")
    else:
        word_name = remove_ext(excel_name) + ".docx"

    word_file_exists = Path(word_name).exists()
    excel_file_exists = Path(excel_name).exists()

    if not excel_file_exists:
        print(colored(f"{excel_name} is not existed."))
        return

    if word_file_exists:
        overwrite = typer.confirm(f"{word_name} is existed, overwrite?")
        if not overwrite:
            return

    #step 1: get which company to make employment certificate
    request1 =  getJsonData(excel_name)
    r1 = session.post(URL + "case/get_companies", json=request1)
    if r1.status_code == 200:
        companies=r1.json()
        for index,company in enumerate(companies):
            print(f"{index}: {company}")
        company_index=int(input("Please input the index of company for employment certificate: "))
        company=companies[company_index]
        #step 2: get the company's certificate
        request2={
            "data":request1,
            "company":company
        }
        r2=session.post(URL + "case/get_certificate", json=request2)
        if r2.status_code == 200:
            with open(word_name, "wb") as f:
                f.write(r2.content)
            console.print(f"{word_name} has been downloaded from web", style=success_style)
        else:
            print_errors(r2)
    else:
        print_errors(r1)
    
        
if __name__ == "__main__":
    app()
