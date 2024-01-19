const searchField = document.querySelector('#searchField')
const tableEmpty = document.querySelector('.table-empty')
const tableNotEmpty = document.querySelector('.table-not-empty')
const pagination = document.querySelector('.pagination-container')
const tbody = document.querySelector('.empty-table-body')


tableEmpty.style.display = 'none';

searchField.addEventListener('keyup', (e)=> {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    pagination.style.display = 'none';
    tbody.innerHTML = '';

    fetch('/incomes/search-incomes', {
      body: JSON.stringify({searchText: searchValue}),
      method: "POST",
    })
    .then(res => res.json())
    .then(data => {
      console.log(data)
      tableNotEmpty.style.display = 'none';
      tableEmpty.style.display = 'block';
      if (data.length === 0) {
        tbody.innerHTML = 'No result found'
      } else {
        // add seached item to the empty table one by one
        data.forEach(item => {
          tbody.innerHTML+=`
          <tr>
            <td>${item.amount}</td>
            <td>${item.category}</td>
            <td>${item.description}</td>
            <td>${item.date}</td>
          </tr>
          `
        })
      }
    })
  } else {
    tableEmpty.style.display = 'none';
    tableNotEmpty.style.display = 'block';
    pagination.style.display = 'block';
  }
})