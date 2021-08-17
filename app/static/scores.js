function search(event) {
    // if (event.keyCode == 13) {
        // declare variables
        var input, filter, tr, td, txtValue, table;
        // get input and table rows
        input = document.getElementById('search');
        filter = input.value.toLowerCase().trim();
        table = document.getElementById("all_info");
        tr = table.getElementsByTagName("tr");
        count = 0;
        for (i = 0; i < tr.length; i++) {
            // take the form class and name value from the cell
            console.log(tr[i])
            _nameTag = tr[i].getElementsByTagName("td")[0];
            _formTag = tr[i].getElementsByTagName("td")[1];
            if (_nameTag && _formTag) {
                _name = _nameTag.textContent || _nameTag.innerText;
                _form = _formTag.textContent || _formTag.innerText;
                // if input in those cells, display = block, else hide. 
                if (_name.toLowerCase().indexOf(filter) > -1 || _form.toLowerCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
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
// }

function getIndex(col_name) {
    // return index base on column name
    switch(col_name) {
        case 'year_level': return 2;
        case 'house': return 3;
        case 'game_status': return 5;
    }
}

function filter(category, filter) {
    // get all rows and filter value
    table = document.getElementById("all_info");
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
    table = document.getElementById('all_info');
    tr = table.getElementsByTagName("tr");
    // change all rows to display, background color according to css
    for (i = 0; i < tr.length; i++) {
        tr[i].style.display = "";
        tr[i].style.backgroundColor = "";
    }
}

function headerClick(header) {
    // declare variables
    var table, rows, tbody, index, allData, newTable;
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
    tbody = table.getElementsByTagName("tbody")[0];
    rows = tbody.children;
    allData = [];
    for (let i = 0; i < rows.length; i++) {
        allData.push([]);
        const row = rows[i].children;
        for (let j = 0; j < row.length; j++) {
            const cell = row[j];
            allData[i].push(cell.innerText);
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