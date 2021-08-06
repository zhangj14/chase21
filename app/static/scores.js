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