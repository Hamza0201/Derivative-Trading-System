<?php
if (!isset($_POST['date']) || $_POST['date'] == "") {
  header('Location: ./');
}

$date = $_POST['date'];

include '../callAPI.php';
$trades =  callAPI('GET', 'http://localhost:5002/getReport/'.$date, false);
$trades = json_decode($trades, true);

require('../fpdf/fpdf.php');

class PDF extends FPDF
{
  var $widths;
  var $rowFill;
  var $isTrades;

  function Header()
  {
      global $title;

      // Arial bold 15
      $this->SetFont('Arial','B',30);
      // Calculate width of title and position
      $w = $this->GetStringWidth($title)+6;
      $this->SetXY(0, 0);
      // Colors of frame, background and text
      $this->SetFillColor(0,80,180);
      $this->SetTextColor(0,0,0);
      // Thickness of frame (1 mm)
      $this->SetLineWidth(1);
      // Title
      $this->Cell($this->GetPageWidth(),30,$title,0,2,'C',true);
      // Line break
      $this->Ln(5);
      //Table headers
      if ($this->isTrades) {
        $this->SetFont('Arial','B', 10);
        $this->SetLineWidth(0.3);
        $this->SetFillColor(150, 220, 255);
        $this->rowFill = True;
        $this->Row(array("Trade ID", "Date Placed", "Maturity Date", "Product",
          "Quantity", "Buying Party", "Selling Party", "Underlying Currency",
          "Underlying Price", "Notional Currency", "Notional Price", "Strike Price"
        ), 'C');
        $this->rowFill = False;
      } else {
        $this->SetFont('Arial','B', 15);
        $this->Cell($this->GetPageWidth(),15,"No trades made on chosen date.",0,2,'C');
      }
  }

function Footer()
{
    // Position at 1.5 cm from bottom
    $this->SetY(-15);
    // Arial italic 8
    $this->SetFont('Arial','I',8);
    // Text color in gray
    $this->SetTextColor(128);
    // Page number
    $this->Cell(0,10,'Page '.$this->PageNo(),0,0,'C');
}

//Adapted from http://fpdf.org/en/script/script3.php
function SetWidths($w)
{
    //Set the array of column widths
    $this->widths=$w;
}

function Row($data, $align)
{
    //Calculate the height of the row
    $nb=0;
    for($i=0;$i<count($data);$i++)
        $nb=max($nb,$this->NbLines($this->widths[$i],$data[$i]));
    $h=5*$nb;
    //Issue a page break first if needed
    $this->CheckPageBreak($h);
    //Draw the cells of the row
    for($i=0;$i<count($data);$i++)
    {
        $w=$this->widths[$i];
        //Save the current position
        $x=$this->GetX();
        $y=$this->GetY();
        //Draw the border
        if ($this->rowFill) {
          $this->Rect($x,$y,$w,$h,'DF');
        } else {
          $this->Rect($x,$y,$w,$h);
        }
        //Print the text
        $this->MultiCell($w,5,$data[$i],0,$align);
        //Put the position to the right of the cell
        $this->SetXY($x+$w,$y);
    }
    //Go to the next line
    $this->Ln($h);
}

function CheckPageBreak($h)
{
    //If the height h would cause an overflow, add a new page immediately
    if($this->GetY()+$h>$this->PageBreakTrigger)
        $this->AddPage($this->CurOrientation);
}

function NbLines($w,$txt)
{
    //Computes the number of lines a MultiCell of width w will take
    $cw=&$this->CurrentFont['cw'];
    if($w==0)
        $w=$this->w-$this->rMargin-$this->x;
    $wmax=($w-2*$this->cMargin)*1000/$this->FontSize;
    $s=str_replace("\r",'',$txt);
    $nb=strlen($s);
    if($nb>0 and $s[$nb-1]=="\n")
        $nb--;
    $sep=-1;
    $i=0;
    $j=0;
    $l=0;
    $nl=1;
    while($i<$nb)
    {
        $c=$s[$i];
        if($c=="\n")
        {
            $i++;
            $sep=-1;
            $j=$i;
            $l=0;
            $nl++;
            continue;
        }
        if($c==' ')
            $sep=$i;
        $l+=$cw[$c];
        if($l>$wmax)
        {
            if($sep==-1)
            {
                if($i==$j)
                    $i++;
            }
            else
                $i=$sep+1;
            $sep=-1;
            $j=$i;
            $l=0;
            $nl++;
        }
        else
            $i++;
    }
    return $nl;
}

}

$pdf = new PDF();
$pdf->isTrades = !empty($trades);
$title = 'Derivative Trade Report '.$date;
$pdf->SetTitle($title);
$pdf->SetWidths(array(40, 22, 22, 40, 20, 18, 18, 21, 21, 20, 20, 17));
$pdf->SetAuthor('Derivative Trade Monitor');
$pdf->AddPage('L');
//Table of trades
$pdf->SetFont('Arial','', 10);
$pdf->SetFillColor(224,235,255);
foreach($trades as $trade) {
  $pdf->Row(array($trade["tradeID"],$trade["datePlaced"],
      $trade["maturityDate"],$trade["product"],$trade["quantity"],
      $trade["buyingParty"],$trade["sellingParty"], $trade["underlyingCurrency"],
      $trade["underlyingPrice"],$trade["notionalCurrency"],$trade["notionalPrice"],
      $trade["strikePrice"]
    ), 'L');
  $pdf->rowFill = !$pdf->rowFill;
}

$pdf->Output();

?>
