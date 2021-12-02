<!DOCTYPE html>
<?php
$tradeID = $_GET["tradeID"];
include '../callAPI.php';
$currencies =  callAPI('GET', 'http://localhost:5002/getCurrencies', false);
$currencies = json_decode($currencies, true);

//Get trade info to be edited
$tradeInfo = callAPI('GET', 'http://localhost:5002/getTrade/'.$tradeID, false);
$tradeInfo = json_decode($tradeInfo, true);
?>

<html>
<head>
  <title>Derivative Monitor</title>
   <meta charset="UTF-8">
  <link rel="stylesheet" href="../css/main.css">
  <link rel="icon" href="../images/Icon.svg">
  <link href="https://fonts.googleapis.com/css?family=Ubuntu&display=swap" rel="stylesheet">
  <script src="../js/input-validator.js"></script>
  <script src="../js/alter-trade.js"></script>
  <script src="../js/delete-trade.js"></script>
</head>
<body id = "alter">
  <div id = "particles-js"></div>
  <div class = "main centreColumn">
    <?php include '../navigation.php' ?>
    <section id = "alter">
      <div class = "greyBackground blueBorder">
        <h2>Alter Trade Information</h2>
        <form class="tradeForm" onsubmit="alterTrade();return false">
          <!-- Not sure they will actually enter the ID or not -->
          <p>
            <label>TRADE ID:</label>
            <input id="tradeID" disabled value="<?php echo $tradeID ?>" type = "text" placeholder="Trade ID">
          </p>
          <p>
            <label>DATE PLACED:</label>
            <input id="datePlace" disabled value="<?php echo $tradeInfo["datePlaced"]?>" type = "text" class = "date" placeholder="Placed"
              onfocus="(this.type='date')"
              onblur="(this.type='text')">
          </p>
          <p>
            <label>MATURITY DATE:</label>
            <input id="maturityDate" value="<?php echo $tradeInfo["maturityDate"]?>" type = "text" class = "date" placeholder="Maturity"
              onfocus="(this.type='date')"
              onblur="(this.type='text')">
          </p>
          <p>
            <label>PRODUCT</label>
            <input id="product" value="<?php echo $tradeInfo["product"]?>" type = "text" placeholder="Product" pattern="([\w ]+)" title="No special characters are used">
          </p>
          <p>
            <label>QUANTITY:</label>
            <input id="quantity" value="<?php echo $tradeInfo["quantity"]?>" type = "number" placeholder="Quantity" min="1">
          </p>
          <p>
            <label>BUYING:</label>
            <input id="buyingParty" value="<?php echo $tradeInfo["buyingParty"]?>" type = "text" placeholder="Buying" pattern="([A-z 0-9])*" title="a company code">
          </p>
          <p>
            <label>SELLING:</label>
            <input id="sellingParty" value="<?php echo $tradeInfo["sellingParty"]?>" type = "text" placeholder="Selling" pattern="([A-z 0-9])*" title="a company code">
          </p>
          <p>
            <label>NOTIONAL VALUE:</label>
            <select id="currenyNotional" class = "Currency">
              <?php
              foreach($currencies as $currency) {
                if ($currency == $tradeInfo["notionalCurrency"]) {
                    echo '"<option value="'.$currency.'" selected="selected">'.$currency.'</option>"';
                } else {
                    echo '"<option value="'.$currency.'">'.$currency.'</option>"';
                }
              }
              ?>
            </select>
            <input id="priceNotional" value="<?php echo $tradeInfo["notionalPrice"]?>" type = "text" placeholder="Price" pattern="[1-9][0-9]*|[0-9][0-9]*.[0-9]*[1-9]|[1-9][0-9]*.[0-9]+" title="a number larger than 0">
          </p>
          <p>
              <label>UNDERLYING VALUE:</label>
              <select id="currenyUnder" class = "Currency">
                <?php
                  foreach($currencies as $currency) {
                    if ($currency == $tradeInfo["underlyingCurrency"]) {
                        echo '"<option value="'.$currency.'" selected="selected">'.$currency.'</option>"';
                    } else {
                        echo '"<option value="'.$currency.'">'.$currency.'</option>"';
                    }
                  }
                ?>
              </select>
              <input id="priceUnder" value="<?php echo $tradeInfo["underlyingPrice"]?>" type = "text" placeholder="Price" pattern="[1-9][0-9]*|[0-9][0-9]*.[0-9]*[1-9]|[1-9][0-9]*.[0-9]+" title="a number larger than 0">
          </p>
          <p>
            <label>STRIKE PRICE:</label>
            <input id="strikePrice" value="<?php echo $tradeInfo["strikePrice"]?>" type = "text" placeholder="Strike Price" pattern="[1-9][0-9]*|[0-9][0-9]*.[0-9]*[1-9]|[1-9][0-9]*.[0-9]+" title="a number larger than 0">
          </p>
          <p>
            <button type="button" onclick="deleteTrade(); return false">Delete Trade</button>
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
