from django.shortcuts import render
from .forms import ResultTable
from main import fill_the_table, metrics

def parser_page(request):
    operands, operators = None, None

    if request.method == "POST":
        form = ResultTable(request.POST)
        with open("file.txt") as file:
             input_text = file.read()
             operands, operators = fill_the_table(input_text)
             str = metrics(input_text)
        form = ResultTable(initial={'code': input_text})


    else:
        # Чтение содержимого файла и передача его в форму при первой загрузке страницы
        with open("file.txt") as file:
            input_text = file.read()
            operands, operators = fill_the_table(input_text)
            str = metrics(input_text)
        form = ResultTable(initial={'code': input_text})

    data = {
        "form": form,
        "operands": operands,
        "operators": operators,
        "result_str": str
    }
    return render(request, "testParser/index.html", data)
