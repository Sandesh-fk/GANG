document.getElementById('geo-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const geo = document.getElementById('geo').value;
    const group_col = document.getElementById('group_col').value;
    const group1 = document.getElementById('group1').value;
    const group2 = document.getElementById('group2').value;
    const top_n = document.getElementById('top_n').value;
    const res = await fetch(`/api/de_genes?geo=${geo}&group_col=${group_col}&group1=${group1}&group2=${group2}&top_n=${top_n}`);
    const data = await res.json();
    const tbody = document.querySelector('#results-table tbody');
    tbody.innerHTML = '';
    if (data.error) {
        alert('Error: ' + data.error);
        return;
    }
    data.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${row.gene}</td><td>${row.p_value.toExponential(2)}</td>
                        <td>${row['mean_' + group1].toFixed(2)}</td>
                        <td>${row['mean_' + group2].toFixed(2)}</td>`;
        tbody.appendChild(tr);
    });
});
