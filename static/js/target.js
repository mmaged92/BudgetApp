// function showhide() {
//     const freq = document.getElementById("id_frequency").value;
//     const monthly = document.getElementById("month_input");

//     if (freq === "monthly") {
//         monthly.style.display = "inline";
//     }

//     if (freq === "annually") {
//         monthly.style.display = "none";
//     }

// }

// document.getElementById('id_frequency').addEventListener('change', showhide)

async function fetchcategories() {

    const response = await fetch('/trans/keyword/category', { method: 'GET' });
    const category_list = await response.json();
    return category_list;
}

async function fetchData() {
    const reponse = await fetch('/target/targetinsert/all', { method: 'GET' });
    const target_list = await reponse.json();
    return target_list
}

async function fetchmonth() {
    const reponse = await fetch('/target/targetinsert/monthget', { method: 'GET' });
    const data = await reponse.json();
    return data
}

async function fetchyears() {
    const reponse = await fetch('/target/targetinsert/yearget', { method: 'GET' });
    const data = await reponse.json();
    return data
}
async function fetchfreq() {
    const reponse = await fetch('/target/targetinsert/freqget', { method: 'GET' });
    const data = await reponse.json();
    return data
}


async function confirm_delete_target(target_id) {
    // console.log(input) 
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;
    console.log(target_id)
    // const reqBody = {keyword_id}

    const response = await fetch('/target/targetinsert/delete', {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ target_id }),
    });
    window.location.reload();
}

async function category_update_target(newValue, category_id, target_id) {
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    const response = await fetch('/target/targetinsert/category_update_target', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ newValue, category_id, target_id }),
    })
    window.location.reload();
}

async function tagert_update(newValue, target_id) {
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    const response = await fetch('/target/targetinsert/target_update', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ newValue, target_id }),
    })
    window.location.reload();
}
async function month_update(newValue, year, month_id, target_id, frequency) {
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    const response = await fetch('/target/targetinsert/monthupdate', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ newValue, year, month_id, target_id, frequency }),
    })
    window.location.reload();
}

async function year_update(newValue, year_id, month, target_id) {
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    const response = await fetch('/target/targetinsert/yearupdate', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ newValue, year_id, month, target_id }),
    })
    window.location.reload();
}
async function freq_update(newValue, target_id, year, month) {
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    const response = await fetch('/target/targetinsert/freq_update', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ newValue, target_id, year, month }),
    })
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
    const myCategoryList = await fetchcategories();
    const months = await fetchmonth();
    const years = await fetchyears();
    const freq = await fetchfreq();
    const gridOptions = {

        rowData: [],

        columnDefs: [

            {
                field: "year", filter: true, editable: true,
                cellEditor: "agSelectCellEditor",
                cellEditorParams: {
                    values: years
                }
            },
            {
                field: "month", filter: true, editable: true,
                cellEditor: "agSelectCellEditor",
                cellEditorParams: {
                    values: months
                }
            },
            {
                field: "category",
                filter: true,
                editable: true,
                cellEditor: "agSelectCellEditor",
                cellEditorParams: {
                    values: myCategoryList
                }
            },
            { field: "target", filter: true, editable: true },
            {
                field: "frequency", filter: true, editable: true,
                cellEditor: "agSelectCellEditor",
                cellEditorParams: {
                    values: freq
                }
            },
            { field: "category_id", hide: true },
            { field: "target_id", hide: true },
            { field: "year_id", hide: true },
            { field: "month_id", hide: true },
            {
                field: " ", cellRenderer: params => {
                    const deleteIcon = `<i class="fa-solid fa-trash"  onclick="confirm_delete_target(${params.data.target_id})"></i>`
                    return `${deleteIcon} `;
                }
            }
        ],
        rowSelection: {
            mode: 'multiRow'
        },
        onCellValueChanged: params => {

            if (params.colDef.field === 'category') {
                category_update_target(params.newValue, params.data.category_id, params.data.target_id)
            }
            if (params.colDef.field === 'frequency') {
                freq_update(params.newValue, params.data.target_id, params.data.year, params.data.month)
            }
            if (params.colDef.field === 'target') {
                tagert_update(params.newValue, params.data.target_id)
            }
            if (params.colDef.field === 'year') {
                year_update(params.newValue, params.data.year_id, params.data.month, params.data.target_id)
            }
            if (params.colDef.field === 'month') {
                month_update(params.newValue, params.data.year, params.data.month_id, params.data.target_id, params.data.frequency)
            }
        }

    }


    const myGridElement = document.querySelector('#myGridtarget');
    gridApi = agGrid.createGrid(myGridElement, gridOptions);


    fetchData().then((Data) => {
        gridApi.setGridOption('rowData', Data)
    });

}
initGrid();


document.getElementById('deletealltarget').addEventListener('click', () => {
    const selectedData = gridApi.getSelectedRows().map(row => row.target_id);
    console.log(selectedData);
    confirm_delete_target(selectedData);
});