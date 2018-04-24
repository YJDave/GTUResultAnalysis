	function dynamicdropdown(listindex)
{
    switch (listindex)
    {
    case "bs1reg" :
        document.formname.status.options[0]=new Option("Select status","");
        document.formname.status.options[1]=new Option("OPEN","open");
        document.formname.status.options[2]=new Option("DELIVERED","delivered");
        break;
    case "bs2reg" :
			document.formname.status.options[0]=new Option("Select status","");
			document.formname.status.options[1]=new Option("OPEN","open");
			document.formname.status.options[2]=new Option("DELIVERED","delivered");
        break;
    }
    return true;
}
function configureDropDownLists(ddl1,ddl2) {
    var w17 = ['BE SEM 1 - Regular (DEC 2017)','BE SEM 1 - Remedial (DEC 2017)','BE SEM 2 - Remedial (DEC 2017)','BE SEM 3 - Regular (DEC 2017)','BE SEM 3 - Remedial (DEC 2017)','BE SEM 4 - Remedial (DEC 2017)','BE SEM 5 - Regular (DEC 2017)','BE SEM 5 - Remedial (DEC 2017)','BE SEM 6 - Remedial (DEC 2017)','BE SEM 7 - Regular (DEC 2017)','BE SEM 7 - Remedial (DEC 2017)','BE SEM 8 - Remedial (DEC 2017)'];
    var s17 = ['BE SEM 1 - Remedial (MAY 2017)','BE SEM 2 - Regular (MAY 2017)','BE SEM 2 - Remedial (MAY 2017)','BE SEM 3 - Remedial (MAY 2017)','BE SEM 4 - Regular (MAY 2017)','BE SEM 4 - Remedial (MAY 2017)','BE SEM 5 - Remedial (MAY 2017)','BE SEM 6 - Regular (MAY 2017)','BE SEM 6 - Remedial (MAY 2017)','BE SEM 7 - Remedial (MAY 2017)','BE SEM 8 - Regular (MAY 2017)','BE SEM 8 - Remedial (MAY 2017)'];
    var w18 = ['BE SEM 1 - Regular (DEC 2018)','BE SEM 1 - Remedial (DEC 2018)','BE SEM 2 - Remedial (DEC 2018)','BE SEM 3 - Regular (DEC 2018)','BE SEM 3 - Remedial (DEC 2018)','BE SEM 4 - Remedial (DEC 2018)','BE SEM 5 - Regular (DEC 2018)','BE SEM 5 - Remedial (DEC 2018)','BE SEM 6 - Remedial (DEC 2018)','BE SEM 7 - Regular (DEC 2018)','BE SEM 7 - Remedial (DEC 2018)','BE SEM 8 - Remedial (DEC 2018)'];

    switch (ddl1.value) {
        case 'w17':
            ddl2.options.length = 0;
            for (i = 0; i < w17.length; i++) {
                createOption(ddl2, w17[i], w17[i]);
            }
            break;
        case 's17':
            ddl2.options.length = 0; 
        for (i = 0; i < s17.length; i++) {
            createOption(ddl2, s17[i], s17[i]);
            }
            break;
        case 'w18':
            ddl2.options.length = 0;
            for (i = 0; i < w18.length; i++) {
                createOption(ddl2, w18[i], w18[i]);
            }
            break;
            default:
                ddl2.options.length = 0;
            break;
    }

}

    function createOption(ddl, text, value) {
        var opt = document.createElement('option');
        opt.value = value;
        opt.text = text;
        ddl.options.add(opt);
    }
    