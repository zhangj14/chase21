function search(event) {
    if (event.code === "Enter") {
        // declare variables
        var filter, rows;
        // get input and table rows
        filter = document.getElementById('search').value.toLowerCase().trim();
        rows = document.getElementById("all_info").getElementsByTagName("tr");
        count = 0;
        for (i = 0; i < rows.length; i++) {
            // take the form class and name value from the cell
            _fnameTag = rows[i].getElementsByTagName("td")[0];
            _lnameTag = rows[i].getElementsByTagName("td")[1];
            _formTag = rows[i].getElementsByTagName("td")[2];
            if (_fnameTag && _formTag && _lnameTag) {
                _fname = _fnameTag.innerText.toLowerCase();
                _lname = _lnameTag.innerText.toLowerCase();
                _form = _formTag.innerText.toLowerCase();
                // if input in those cells, display = block, else hide. 
                if (_fname.indexOf(filter) > -1 || _form.indexOf(filter) > -1 || _lname.indexOf(filter) > -1) {
                    rows[i].style.display = "";
                    count++;
                    // every second row
                    if (count % 2 == 0) {
                        rows[i].style.backgroundColor = "#fdfdfd";
                    }
                    else {
                        rows[i].style.backgroundColor = "#f0f0f0";
                    }
                } else {
                    rows[i].style.display = "none";
                }
            }
        } 
    }
}

function getIndex(col_name) {
    // return index base on column name
    switch(col_name) {
        case 'year_level': return 3;
        case 'house': return 4;
        case 'game_status': return 6;
    }
}

function filter(category, filter) {
    // get all rows and filter value
    table = document.getElementById("all_info").getElementsByTagName("tbody")[0];
    tr = table.getElementsByTagName("tr");
    filter = filter.toLowerCase().trim();
    count = 0;
    for (i = 0; i < tr.length; i++) {
        // skip already invalid rows
        if (tr[i].style.display != "none") {
            // get value based on the filter's category
            cell = tr[i].getElementsByTagName("td")[getIndex(category)];
            if (cell) {
                value = cell.textContent || cell.innerText;
                if (filter == value.toLowerCase().trim()) {
                    // keep display property
                    tr[i].style.display = "";
                    // add displayed to count
                    count++;
                    // every second row
                    if (count % 2 == 0) {
                        tr[i].style.backgroundColor = "#fdfdfd";
                    }
                    else {
                        tr[i].style.backgroundColor = "#f0f0f0";
                    }
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }
}

function clearFilter() {
    // get html object
    table = document.getElementById('all_info').getElementsByTagName("tbody")[0];
    tr = table.getElementsByTagName("tr");
    // change all rows to display, background color according to css
    for (i = 0; i < tr.length; i++) {
        tr[i].style.display = "";
        tr[i].style.backgroundColor = "";
    }
}

function headerClick(header) {
    // declare variables
    var table, rows, index, allData, newTable;
    // different index for different columns
    switch (header.innerText) {
        case "First name":
            index = 0;
            break;
        case "Last name":
            index = 1;
            break;
        case "Form class":
            index = 2;
            break;
        case "Year level":
            index = 3;
            break;
        case "House":
            index = 4;
            break;
        case "Score":
            index = 5;
            break;
        case "Game status":
            index = 6;
            break;
        default:
            break;
    }
    // get all data rows in the table
    // header -> tr -> thead -> table
    table = header.parentNode.parentNode.parentNode;
    rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");
    allData = [];
    for (let i = 0; i < rows.length; i++) {
        if (rows[i].style.display != 'none') {
            const row = rows[i].getElementsByTagName("td");
            let list = [];
            for (let j = 0; j < row.length; j++) {
                list.push(row[j].innerText);
            }
            allData.push(list);
        }
    }
    // compare function. utf-16 order if text. numeric order if int. 
    function compare(a, b) {
        if (isNaN(a[index])) {
            return a[index].localeCompare(b[index]);
        } else {
            return a[index] - b[index];
        }
    }
    allData.sort(compare);
    newTable = "";
    for (const row of allData) {
        newTable += "<tr>";
        for (const cell of row) {
            newTable += "<td>" + cell + "</td>";
        }
        newTable += "</tr>";
    }
    table.getElementsByTagName("tbody")[0].innerHTML = newTable;
}

function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabscontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}