
async function fetchData() {
    const response = await fetch('/accounts/getaccounts', { method: 'GET' });
    const data = await response.json();
    return data

}
async function fetchBank() {
    const response = await fetch('/accounts/bank_get', { method: 'GET' });
    const data = await response.json();
    return data

}
async function fetchAccountsTypes() {
    const response = await fetch('/accounts/accounttype_get', { method: 'GET' });
    const data = await response.json();
    return data

}

async function confirm_delete_account(account_id) {
    // console.log(input) 
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    // const reqBody = {keyword_id}
    const response = await fetch('/accounts/delete/', {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ account_id }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log(result);
    window.location.reload();
}

async function Bank_update(newValue, account_id) {
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    const response = await fetch('/accounts/bank_update/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({newValue, account_id}),
        
    })

    window.location.reload();
}

async function account_type_update(newValue, account_id) {
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    const response = await fetch('/accounts/accounttype_update/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({newValue, account_id}),
        
    })

    window.location.reload();
}

async function account_name_update(newValue, account_id) {
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    const response = await fetch('/accounts/accountname_update/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({newValue, account_id}),
        
    })

    window.location.reload();
}

async function account_number_update(newValue, account_id) {
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    const response = await fetch('/accounts/accountnumber_update/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({newValue, account_id}),
        
    })

    window.location.reload();
}

async function account_balance_update(newValue, account_id) {
    const isConfirmed = confirm('are you sure?');
    if (!isConfirmed) return;

    const response = await fetch('/accounts/accountbalance_update/', {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({newValue, account_id}),
        
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
    const banks = await fetchBank();
    const accountTypes = await fetchAccountsTypes();

    const gridOptions = {

        rowData: [],

        columnDefs: [

            {
                field: "Bank", filter: true, editable: true,
                cellEditor: "agSelectCellEditor",
                cellEditorParams: {
                values: banks
                }
            },
            {
                field: "account_type", filter: true, editable: true,
                cellEditor: "agSelectCellEditor",
                cellEditorParams: {
                values: accountTypes
                }
            },
            {
                field: "account_name",
                filter: true,
                editable: true,
            },
            { field: "account_number", filter: true, editable: true },
            { field: "account_balance", filter: true, editable: true },

            { field: "account_id", hide: true },
            {
                field: " ", cellRenderer: params => {
                    const deleteIcon = `<i class="fa-solid fa-trash"  onclick="confirm_delete_account(${params.data.account_id})"></i>`
                    return `${deleteIcon} `;
                }
            }

        ],
        rowSelection: {
            mode: 'multiRow'
        },
        onCellValueChanged: params => {

            if (params.colDef.field === 'Bank') {
                Bank_update(params.newValue, params.data.account_id)
            }
            if (params.colDef.field === 'account_type') {
                account_type_update(params.newValue, params.data.account_id)
            }
            if (params.colDef.field === 'account_name') {
                account_name_update(params.newValue, params.data.account_id)
            }
            if (params.colDef.field === 'account_number') {
                account_number_update(params.newValue, params.data.account_id)
            }
            if (params.colDef.field === 'account_balance') {
                account_balance_update(params.newValue, params.data.account_id)
            }
        }

    }


    const myGridElement = document.querySelector('#myGridaccounts');
    gridApi = agGrid.createGrid(myGridElement, gridOptions);


    fetchData().then((Data) => {
        gridApi.setGridOption('rowData', Data)
    });

}
initGrid();


document.getElementById('deleteallaccounts').addEventListener('click', () => {
    const selectedData = gridApi.getSelectedRows().map(row => row.account_id);
    confirm_delete_account(selectedData);
});