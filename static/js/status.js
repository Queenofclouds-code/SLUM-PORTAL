function updateStatus(department, slumId, newStatus) {
    let url = "";

    switch (department) {
        case "admin":
            url = "/slum-portal/api/update/admin-status";
            break;
        case "demography":
            url = "/slum-portal/api/update/demography-status";
            break;
        case "legal":
            url = "/slum-portal/api/update/legal-status";
            break;
        case "infrastructure":
            url = "/slum-portal/api/update/infrastructure-status";
            break;
        case "housing":
            url = "/slum-portal/api/update/housing-status";
            break;
        case "gis":
            url = "/slum-portal/api/update/gis-status";
            break;
        default:
            alert("Invalid department");
            return;
    }

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            slum_id: slumId,
            status: newStatus
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert("Status update failed");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Server error");
    });
}
