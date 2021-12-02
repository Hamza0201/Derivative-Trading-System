<!DOCTYPE html>
<?php
  include '../callAPI.php';
  $currencies =  callAPI('GET', 'http://localhost:5002/getCurrencies', false);
  $currencies = json_decode($currencies, true);

  $currentDate = date("Y-m-d");
 ?>

<html>
<head>
  <title>Derivative Monitor</title>
   <meta charset="UTF-8">
  <link rel="stylesheet" href="../css/main.css">
  <link rel="icon" href="../images/Icon.svg">
  <link href="https://fonts.googleapis.com/css?family=Ubuntu&display=swap" rel="stylesheet">
  <script src="../js/filter-trades.js"></script>
  <script src="../js/show-more.js"></script>
</head>
<body id = "alter">
  <div id = "particles-js"></div>
  <div class = "main centreColumn">
    <?php include '../navigation.php'?>
    <section id = "filter">
      <div class ="collapsibleBackground blueBorder">
        <div class="collapsible">
          <h2>Filters</h2>
          <div class="plus">+</div>
        </div>
        <div class="content" id="content">
          <form class="tradeForm" id="filterForm" onsubmit="filterTrade();return false">
            <p>
              <label>TRADE ID:</label>
              <input id="tradeID" type = "text" placeholder="Trade ID"><br>
            </p>
            <p>
              <label>DATE PLACED:</label>
              <input id="datePlace" value="<?php echo date("Y-m-d");?>" type = "text" class = "date" placeholder="Placed"
                onfocus="(this.type='date')"
                onblur="(this.type='text')">
            </p>
            <p>
              <label>MATURITY DATE:</label>
              <input id="maturityDate" type = "text" class = "date" placeholder="Maturity"
                onfocus="(this.type='date')"
                onblur="(this.type='text')">
            </p>
            <p>
              <label>PRODUCT</label>
              <input id="product" type = "text" placeholder="Product" pattern="([\w ]+)" title="No special characters are used">
            </p>
            <p>
              <label>QUANTITY:</label>
              <input id="quantity" type = "text" placeholder="Quantity" pattern="[1-9]([0-9])*" title="an integer greater than 1">
            </p>
            <p>
              <label>BUYING:</label>
              <input id="buyingParty" type = "text" placeholder="Buying" pattern="([A-z 0-9])*" title="a company code">
            </p>
            <p>
              <label>SELLING:</label>
              <input id="sellingParty" type = "text" placeholder="Selling" pattern="([A-z 0-9])*" title="a company code">
            </p>
            <p>
              <label>NOTIONAL VALUE:</label>
              <select id="currenyNotional" class = "Currency">
                <option value="null" selected="selected">N/A</option>
                <?php
                  foreach($currencies as $currency) {
                    echo '"<option value="'.$currency.'">'.$currency.'</option>"';
                  }
                ?>
              </select>
              <input id="priceNotional" type = "text" placeholder="Price" pattern="[1-9][0-9]*|[0-9][0-9]*.[0-9]*[1-9]|[1-9][0-9]*.[0-9]+" title="a number larger than 0">
            </p>
            <p>
                <label>UNDERLYING VALUE:</label>
                <select id="currenyUnder" class = "Currency">
                  <option value="null" selected="selected">N/A</option>
                  <?php
                    foreach($currencies as $currency) {
                      echo '"<option value="'.$currency.'">'.$currency.'</option>"';
                    }
                  ?>
                </select>
                <input id="priceUnder" type = "text" placeholder="Price" pattern="[1-9][0-9]*|[0-9][0-9]*.[0-9]*[1-9]|[1-9][0-9]*.[0-9]+" title="a number larger than 0">
            </p>
            <p>
              <label>STRIKE PRICE:</label>
              <input id="strikePrice" type = "text" placeholder="Strike Price" pattern="[1-9][0-9]*|[0-9][0-9]*.[0-9]*[1-9]|[1-9][0-9]*.[0-9]+" title="a number larger than 0">
            </p>
            <p class="full-width">
              <input type = "submit" value = "Submit">
            </p>
          </form>
        </div>
      </div>
    </section>
    <section id = "transactions">
      <?php
        $trades =  callAPI('GET', 'http://localhost:5002/filterTrades/0/null/'.$currentDate.'/null/null/null/null/null/null/null/null/null/null', false);
        $trades = json_decode($trades, true);
      ?>
        <table id = "transTable" <?php if (empty($trades)) {echo 'style="display: none;"';}?>>
          <thead>
              <tr>
                <th>Date</th>
                <th>Product</th>
                <th>Trade ID</th>
                <th>Buying Party</th>
                <th>Selling Party</th>
                <th>Notional Amount</th>
                <th>Quantity</th>
                <th>Notional Currency</th>
                <th>Maturity Date</th>
                <th>Underlying Price</th>
                <th>Underlying Currency</th>
                <th>Strike Price</th>
              </tr>
          </thead>
          <tbody id = 'transBody'>
            <?php
              foreach($trades as $trade) {
                //Makes the row clickable and send the trade id to alter trade page
                if ($currentDate == $trade["datePlaced"]) {
                    echo '<tr onclick="window.location.href=\'alter-trade.php?tradeID='.$trade["tradeID"].'\'">';
                } else {
                    echo '<tr onclick="alert('."'Trade is too old to edit'".')">';
                }
                echo "<td>".$trade["datePlaced"]."</td>";
                echo "<td>".$trade["product"]."</td>";
                echo "<td>".$trade["tradeID"]."</td>";
                echo "<td>".$trade["buyingParty"]."</td>";
                echo "<td>".$trade["sellingParty"]."</td>";
                echo "<td>".$trade["notionalPrice"]."</td>";
                echo "<td>".$trade["quantity"]."</td>";
                echo "<td>".$trade["notionalCurrency"]."</td>";
                echo "<td>".$trade["maturityDate"]."</td>";
                echo "<td>".$trade["underlyingPrice"]."</td>";
                echo "<td>".$trade["underlyingCurrency"]."</td>";
                echo "<td>".$trade["strikePrice"]."</td>";
                echo "</tr>";
              }

              if (!empty($trades)) {
                echo "</tbody>";
              }
             ?>
        </table>
        <div class="wrapper">
          <button id="showMoreButton" onclick="showMoreTrades('<?php echo "2019-04-02" ?>',10)"><?php if (!empty($trades)) { echo "Show More";} else {echo "No Trades on ".$currentDate;}?></button>
        </div>
    </section>

    <!-- scripts -->
    <script src="../particles/particles.js"></script>
    <script src="../particles/app.js"></script>
    <script src="../js/alter.js"></script>
    <script src="../js/collapsible.js"></script>

    </html>
