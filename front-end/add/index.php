<!DOCTYPE html>
<html>
<head>
  <?php
    include '../callAPI.php';
    $currencies =  callAPI('GET', 'http://localhost:5002/getCurrencies', false);
    $currencies = json_decode($currencies, true);
   ?>
  <title>Derivative Monitor</title>
   <meta charset="UTF-8">
  <link rel="stylesheet" href="../css/main.css">
  <link rel="icon" href="../images/Icon.svg">
  <link href="https://fonts.googleapis.com/css?family=Ubuntu&display=swap" rel="stylesheet">
  <script src="../js/input-validator.js"></script>
  <script src="../js/add-trade.js"></script>
</head>
<body id = "add">
  <div id = "particles-js"></div>
  <div class = "main centreColumn">
    <?php include '../navigation.php' ?>
    <section id = "add">
      <div class = "greyBackground blueBorder">
        <h2>Trade Information</h2>
        <form class="tradeForm" id="addForm" onsubmit="addTrade();return false">
          <p>
            <label>DATE PLACED:</label>
            <input id="datePlace" disabled value="<?php echo date("Y-m-d");?>" type = "text" class = "date" placeholder="Placed"
              onfocus="(this.type='date')"
              onblur="(this.type='text')">
          </p>
          <p>
            <label>MATURITY DATE:</label>
            <input id="maturityDate" required type = "text" class = "date" placeholder="Maturity"
              onfocus="(this.type='date')"
              onblur="(this.type='text')">
          </p>
          <p>
            <label>PRODUCT</label>
            <input id="product" required type = "text" placeholder="Product" pattern="([\w ]+)" title="No special characters are used">
          </p>
          <p>
            <label>QUANTITY:</label>
            <input id="quantity" required type = "number" placeholder="Quantity" min="1">
          </p>
          <p>
            <label>BUYING:</label>
            <input id="buyingParty" required type = "text" placeholder="Buying" pattern="([A-z 0-9])*" title="a company code">
          </p>
          <p>
            <label>SELLING:</label>
            <input id="sellingParty" required type = "text" placeholder="Selling" pattern="([A-z 0-9])*" title="a company code">
          </p>
          <p>
            <label>NOTIONAL VALUE:</label>
            <select id="currenyNotional" class = "Currency">
              <?php
                foreach($currencies as $currency) {
                  echo '"<option value="'.$currency.'">'.$currency.'</option>"';
                }
              ?>
            </select>
            <input id="priceNotional" required type = "text" placeholder="Price" pattern="[1-9][0-9]*|[0-9][0-9]*.[0-9]*[1-9]|[1-9][0-9]*.[0-9]+" title="a number larger than 0">
          </p>
          <p>
              <label>UNDERLYING VALUE:</label>
              <select id="currenyUnder" class = "Currency">
                <?php
                  foreach($currencies as $currency) {
                    echo '"<option value="'.$currency.'">'.$currency.'</option>"';
                  }
                ?>
              </select>
              <input id="priceUnder" required type = "text" placeholder="Price" pattern="[1-9][0-9]*|[0-9][0-9]*.[0-9]*[1-9]|[1-9][0-9]*.[0-9]+" title="a number larger than 0">
          </p>
          <p>
            <label>STRIKE PRICE:</label>
            <input id="strikePrice" required type = "text" placeholder="Strike Price" pattern="[1-9][0-9]*|[0-9][0-9]*.[0-9]*[1-9]|[1-9][0-9]*.[0-9]+" title="a number larger than 0">
          </p>
          <p class="full-width">
            <input type = "submit" value = "Submit">
          </p>
        </form>
      </div>
    </section>

    <!-- scripts -->
    <script src="../particles/particles.js"></script>
    <script src="../particles/app.js"></script>

    </html>
