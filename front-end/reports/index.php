<!DOCTYPE html>
<html>
<head>
  <title>Derivative Monitor</title>
   <meta charset="UTF-8">
  <link rel="stylesheet" href="../css/main.css">
  <link rel="icon" href="../images/Icon.svg">
  <link href="https://fonts.googleapis.com/css?family=Ubuntu&display=swap" rel="stylesheet">
</head>
<body id = "reports">
  <div id = "particles-js"></div>
  <div class = "main centreColumn">
    <?php include '../navigation.php' ?>
    <section id = reportSelection>
      <div class = "greyBackground blueBorder">
        <h2>Reports</h2>
        <form class="reportForm" action="getReport.php" method="post">
          <p>
              <label>Report Date:</label>
              <input name="date" type="date" required>
          </p>
          <div class = "submit-wrapper">
            <input type="submit">
          </div>
        </form>
      </div>
    </section>
    <!-- scripts -->
    <script src="../particles/particles.js"></script>
    <script src="../particles/app.js"></script>

    </html>
