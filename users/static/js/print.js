
function preview(oper)
{
    let bdHtml;
    let sprnstr;
    if (oper < 10) {
        bdHtml = window.document.body.innerHTML;//获取当前页的html代码
        sprnstr = "<!--startPrint" + oper + "-->";//设置打印开始区域
        eprnstr = "<!--endPrint" + oper + "-->";//设置打印结束区域
        prnhtml = bdHtml.substring(bdHtml.indexOf(sprnstr) + 18); //从开始代码向后取html
        prnhtml = prnhtml.substring(0, prnhtml.indexOf(eprnstr));//从结束代码向前取html
        window.document.body.innerHTML = prnhtml;
        window.print();
        window.document.body.innerHTML = bdHtml;
    } else {
        window.print();
    }
}

