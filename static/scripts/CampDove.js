 function churchSearch() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("churchSearch");
    filter = input.value.toUpperCase();
    table = document.getElementById("camperTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[2];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }       
    }
  }

  function ShowTab(row) {
    id = row.getAttribute("camper_id");
    fromElementID = 'show_tab_' + id;
    var form = document.getElementById(fromElementID);
    form.submit();
  }

  function valueChanged()
  {
    var nolimit     = document.getElementById("no_limit");
    var weeklylimit = document.getElementById("weekly_limit");
    if(nolimit.checked)
    {
      weeklylimit.value = "";
      weeklylimit.disabled=true;
    }
    else
    {
      weeklylimit.disabled=false;
    }
  }

  function lastNameSearch() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("lastNameSearch");
    filter = input.value.toUpperCase();
    table = document.getElementById("camperTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }       
    }
  }