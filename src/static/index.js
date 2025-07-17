$(function() {
    // Load system information
    $.getJSON('/api/system/info')
        .done(function(data) {
            let html = '<table class="table table-bordered table-striped mt-2">';
            html += '<thead><tr class="table-primary"><th colspan="2" class="text-center">OS</th></tr></thead><tbody>';
            html += `<tr><td>Name</td><td>${data.os.name}</td></tr>`;
            html += '<tr class="table-primary"><th colspan="2" class="text-center">Platform</th></tr>';
            $.each(data.platform, function(key, value) {
                html += `<tr><td>${key.charAt(0).toUpperCase() + key.slice(1)}</td><td>${value}</td></tr>`;
            });
            html += '</tbody></table>';
            $('#info').html(html);
        })
        .fail(function() {
            $('#info').html('<div class="alert alert-danger text-center">Error loading system information.</div>');
        });

    // Load and display disk usage information
    $.getJSON('/api/disk/usage')
        .done(function(data) {
            displayDiskUsageTable(data);
        })
        .fail(function() {
            $('#disk-usage').html('<div class="alert alert-danger text-center">Error loading disk information.</div>');
        });

    // Load and display memory usage information
    $.getJSON('/api/memory/usage')
        .done(function(data) {
            displayMemoryUsageTable(data);
        })
        .fail(function() {
            $('#memory-usage').html('<div class="alert alert-danger text-center">Error loading memory information.</div>');
        });

    // Function to format bytes into readable format
    function formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }

    // Function to display disk usage table
    function displayDiskUsageTable(data) {
        if (!data.disks || data.disks.length === 0) {
            $('#disk-usage').html('<div class="alert alert-warning text-center">No disk information available.</div>');
            return;
        }

        let html = '<table class="table table-bordered table-striped mt-2">';
        html += '<thead><tr class="table-success">';
        html += '<th>Device</th><th>Mount Point</th><th>Total</th><th>Used</th><th>Free</th><th>% Used</th>';
        html += '</tr></thead><tbody>';
        
        data.disks.forEach(function(disk) {
            html += '<tr>';
            html += `<td>${disk.device}</td>`;
            html += `<td>${disk.mountpoint}</td>`;
            html += `<td>${formatBytes(disk.total)}</td>`;
            html += `<td>${formatBytes(disk.used)}</td>`;
            html += `<td>${formatBytes(disk.free)}</td>`;
            html += `<td><div class="progress" style="height: 20px;">`;
            html += `<div class="progress-bar ${disk.percent_used > 90 ? 'bg-danger' : disk.percent_used > 70 ? 'bg-warning' : 'bg-success'}" `;
            html += `role="progressbar" style="width: ${disk.percent_used}%;" `;
            html += `aria-valuenow="${disk.percent_used}" aria-valuemin="0" aria-valuemax="100">${disk.percent_used}%</div>`;
            html += `</div></td>`;
            html += '</tr>';
        });
        
        html += '</tbody></table>';
        $('#disk-usage').html(html);
    }
    
    // Function to display memory usage table
    function displayMemoryUsageTable(data) {
        if (!data || data.error) {
            $('#memory-usage').html('<div class="alert alert-warning text-center">No memory information available.' + 
                                   (data.error ? ` Error: ${data.error}` : '') + '</div>');
            return;
        }

        let html = '<table class="table table-bordered table-striped mt-2">';
        html += '<thead><tr class="table-info"><th colspan="3" class="text-center">Physical Memory</th></tr></thead>';
        html += '<tbody>';
        html += '<tr>';
        html += '<td>Total</td>';
        html += `<td>${formatBytes(data.total)}</td>`;
        html += '<td rowspan="3">';
        html += `<div class="progress" style="height: 100%;">`;
        html += `<div class="progress-bar ${data.percent_used > 90 ? 'bg-danger' : data.percent_used > 70 ? 'bg-warning' : 'bg-info'}" `;
        html += `role="progressbar" style="width: ${data.percent_used}%;" `;
        html += `aria-valuenow="${data.percent_used}" aria-valuemin="0" aria-valuemax="100">${data.percent_used}%</div>`;
        html += '</div>';
        html += '</td>';
        html += '</tr>';
        html += `<tr><td>Used</td><td>${formatBytes(data.used)}</td></tr>`;
        html += `<tr><td>Free</td><td>${formatBytes(data.free)}</td></tr>`;
        
        // Swap section if available
        if (data.swap_total > 0) {
            html += '<tr class="table-info"><th colspan="3" class="text-center">Swap Memory</th></tr>';
            html += '<tr>';
            html += '<td>Total</td>';
            html += `<td>${formatBytes(data.swap_total)}</td>`;
            html += '<td rowspan="3">';
            html += `<div class="progress" style="height: 100%;">`;
            html += `<div class="progress-bar ${data.swap_percent_used > 90 ? 'bg-danger' : data.swap_percent_used > 70 ? 'bg-warning' : 'bg-secondary'}" `;
            html += `role="progressbar" style="width: ${data.swap_percent_used}%;" `;
            html += `aria-valuenow="${data.swap_percent_used}" aria-valuemin="0" aria-valuemax="100">${data.swap_percent_used}%</div>`;
            html += '</div>';
            html += '</td>';
            html += '</tr>';
            html += `<tr><td>Used</td><td>${formatBytes(data.swap_used)}</td></tr>`;
            html += `<tr><td>Free</td><td>${formatBytes(data.swap_free)}</td></tr>`;
        }
        
        html += '</tbody></table>';
        $('#memory-usage').html(html);
    }
});
