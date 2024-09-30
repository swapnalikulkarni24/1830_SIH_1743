document.getElementById('investigate-btn').addEventListener('click', function() {
    // Get selected values
    const platform = document.getElementById('platform').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const reason = document.getElementById('reason-select').value;

    // Check if all fields are filled
    if (!username || !password || !platform || !reason) {
        alert("Please fill all fields before starting the investigation.");
        return;
    }

    // Simulate Investigation Findings
    const reportContent = `
        Investigation Report:
        Platform: ${platform}
        Username: ${username}
        Reason for Investigation: ${reason}

        Findings:
        - Screenshots of selected posts
        - List of all friends
        - Screenshots of objectionable messages with receivers' names
        - List of all comments, etc.
    `;

    document.getElementById('report-content').innerText = reportContent;

    // Generate and Download PDF using jsPDF
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.setFontSize(12);
    doc.text("Social Media Investigation Report", 10, 10);
    doc.text(`Platform: ${platform}`, 10, 20);
    doc.text(`Username: ${username}`, 10, 30);
    doc.text(`Reason for Investigation: ${reason}`, 10, 40);
    doc.text("Findings:", 10, 50);
    doc.text("- Screenshots of selected posts", 10, 60);
    doc.text("- List of all friends", 10, 70);
    doc.text("- Screenshots of objectionable messages", 10, 80);
    doc.text("- List of all comments, etc.", 10, 90);

    // Save the generated PDF
    doc.save("instagram_report.pdf");
});
