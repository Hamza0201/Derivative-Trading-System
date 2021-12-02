<!DOCTYPE html>
<?php
  include '../callAPI.php';
  $warnings =  callAPI('GET', 'http://localhost:5002/warningrules', false);
  $warnings = json_decode($warnings, true);
  $training =  callAPI('GET', 'http://localhost:5002/trainingMode', false);
  $training = json_decode($training, true);
 ?>
<html>
<head>
  <title>Derivative Monitor</title>
   <meta charset="UTF-8">
  <link rel="stylesheet" href="../css/main.css">
  <link rel="icon" href="../images/Icon.svg">
  <link href="https://fonts.googleapis.com/css?family=Ubuntu&display=swap" rel="stylesheet">
  <script src="../js/change-training-mode.js"></script>
  <script src="../js/delete-rules.js"></script>
</head>
<body id = "rules">
  <div id = "particles-js"></div>
  <div class = "main centreColumn">
    <?php include '../navigation.php' ?>
    <section>
      <div class ="collapsibleBackground blueBorder">
        <div class="collapsible">
          <h2>Model Training</h2>
          <div class="plus">+</div>
        </div>
        <div class="content">
          <?php
            if ($training) {
              echo "<p>Training mode is currently enabled.</p>";
              echo "<button onclick='changeMode(); return false'>Disable Training Mode</button>";
            } else {
              echo "<p>Training mode is currently disabled</p>";
              echo "<button onclick='changeMode(); return false'>Enable Training Mode</button>";
            }
          ?>
        </div>
      </div>
    </section>
    <section>
      <div class="collapsible collapsibleBackground blueBorder">
        <h2>Warnings</h2>
        <div class="plus">+</div>
      </div>
      <div class="content">
        <table id="warningsTable" <?php if (empty($warnings)) {echo 'style="display: none;"';}?>>
          <thead>
            <tr>
              <th>Trade ID</th>
              <th>Notional Value</th>
              <th>Predicted Upper</th>
              <th>Predicted Lower</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <?php
            foreach($warnings as $warning) {
              //Makes the row clickable and send the trade id to alter trade page
              echo '<tr>';
              echo "<td>".$warning["tradeID"]."</td>";
              echo "<td>".$warning["notionalVal"]."</td>";
              echo "<td>".$warning["predictedUpper"]."</td>";
              echo "<td>".$warning["predictedLower"]."</td>";
              echo "<td><button onclick='deleteWarning(\"".$warning["tradeID"]."\",".$warning["notionalVal"].",".$warning["predictedUpper"].",".$warning["predictedLower"]."); return false'>Delete</button></td>";
              echo "</tr>";
            }
            ?>
          </tbody>
        </table>
        <div class="wrapper" <?php if (!empty($warnings)) {echo 'style="display: none;"';}?>>
          <button style="cursor:default;">No Warnings</button>
        </div>
      </div>
    </section>

    <!-- scripts -->
    <script src="../particles/particles.js"></script>
    <script src="../particles/app.js"></script>
    <script src="../js/collapsible.js"></script>
    <script src="../js/rules.js"></script>

    </html>
