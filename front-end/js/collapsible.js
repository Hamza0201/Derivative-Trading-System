var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var plusMinus = this.getElementsByClassName("plus")
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
      plusMinus[0].innerHTML = "+";
    } else {
      content.style.display = "block";
      plusMinus[0].innerHTML = "-";
    }
  });
}
