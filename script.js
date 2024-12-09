// Dummy Data for Drone Status Table
const droneData = [
    { id: "Drone-1", battery: 85, status: "Active" },
    { id: "Drone-2", battery: 90, status: "Active" },
    { id: "Drone-3", battery: 45, status: "Down" },
    { id: "Drone-4", battery: 60, status: "Active" },
    { id: "Drone-5", battery: 30, status: "Inactive" },
  ];
  
  const droneTableBody = document.getElementById("drone-table-body");
  droneData.forEach((drone) => {
    const row = document.createElement("tr");
    row.innerHTML = `<td>${drone.id}</td><td>${drone.battery}%</td><td>${drone.status}</td>`;
    droneTableBody.appendChild(row);
  });
  
  // Dummy Data for Found People Table
  const peopleData = [
    { name: "John Doe", location: "Sector A" },
    { name: "Jane Smith", location: "Sector C" },
    { name: "Emily Davis", location: "Sector B" },
    { name: "Michael Brown", location: "Sector A" },
    { name: "Anna White", location: "Sector D" },
  ];
  
  const peopleTableBody = document.getElementById("people-table-body");
  peopleData.forEach((person) => {
    const row = document.createElement("tr");
    row.innerHTML = `<td>${person.name}</td><td>${person.location}</td>`;
    peopleTableBody.appendChild(row);
  });
  
  // Handle Simulation File Upload
  const fileInput = document.getElementById("simulation-upload");
  const videoViewer = document.getElementById("simulation-viewer");
  const uploadMessage = document.getElementById("upload-message");
  
  fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      videoViewer.src = url;
      videoViewer.style.display = "block";
      uploadMessage.style.display = "none";
    }
  });
  