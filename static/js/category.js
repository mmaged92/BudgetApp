
async function fetchcategories() {

    const response = await fetch('/target/category_get/');
    const category_list = await response.json();
    return category_list;
}


async function category_update_cat(new_value, category_id) {

    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    const response = await fetch('/target/category_update/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_value, category_id }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log(result);
    window.location.reload();
}

async function fixed_fees_update(new_value, category_id) {

    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;
    console.log(new_value)
    const response = await fetch('/target/fixed_fees_update/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_value, category_id }),

    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log(result);
    window.location.reload();
}


async function confirm_delete(category_id) {
    // console.log(input) 
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    // const reqBody = {keyword_id}
    const response = await fetch('/target/delete/', {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ category_id }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log(result);
    window.location.reload();
}



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


async function initGrid() {
    const gridOptions = {

        rowData: [],

        columnDefs: [
            { field: "Category", filter: true, editable: true },
            {
                field: "fixed_fees", filter: true, editable: true,
                cellDataType: "boolean",
                valueGetter: params => {
                    // Assuming params.data.isActive can be 'True', 'False', or actual booleans
                    console.log(params.data.fixed_fees)
                    if (params.data.fixed_fees === null) {
                        console.log(params.data.fixed_fees)
                        return params.data.fixed_fees === 'false';
                    }
                    else if (params.data.fixed_fees === 'True' || params.data.fixed_fees === 'true'){
                        console.log(params.data.fixed_fees)
                        return params.data.fixed_fees = true // Return as is if already a boolean
                    }
                    else if (params.data.fixed_fees === "False" || params.data.fixed_fees === 'false'){
                        console.log(params.data.fixed_fees)
                        return params.data.fixed_fees = false; // Return as is if already a boolean
                    }
                },
            },
            { field: "category_id", hide: true },
            {
                field: " ", cellRenderer: params => {
                    const deleteIcon = `<i class="fa-solid fa-trash"  onclick="confirm_delete(${params.data.category_id})"></i>`
                    return `${deleteIcon} `;
                }
            }
        ],
        rowSelection: {
            mode: 'multiRow'
        },
        onCellValueChanged: params => {
            if (params.colDef.field === 'Category') {
                category_update_cat(params.newValue, params.data.category_id)
            }
            if (params.colDef.field === 'fixed_fees') {
                fixed_fees_update(params.newValue, params.data.category_id)
            }
        }

    }


    const myGridElement = document.querySelector('#myGridcategories');
    gridApi = agGrid.createGrid(myGridElement, gridOptions);


    fetchcategories().then((category_list) => {
        gridApi.setGridOption('rowData', category_list)
    });

}
initGrid();


document.getElementById('deleteallcategory').addEventListener('click', () => {
    const selectedData = gridApi.getSelectedRows().map(row => row.category_id);
    console.log(selectedData);
    confirm_delete(selectedData);
});