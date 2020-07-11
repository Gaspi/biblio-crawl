
function generate() {
  var panier = document.getElementById("panier");
  var res = new Set();
  panier.childNodes.forEach(function (item, index) {  res.add(item.id)  });
  res.delete('');
  res.delete(undefined);
  window.open("/report?q=" + Array.from(res));
}

function remove_title(id) {
    var panier = document.getElementById("panier");
    panier.childNodes.forEach(function (item, index) {
      if (item.id == id) {
        panier.removeChild(item);
      }
    });
}

function add_title(title,id) {
    var panier = document.getElementById("panier");
    var li=document.createElement('li');
    li.id=id
    var btn = document.createElement("input");
    btn.type="button"
    btn.value="Supprimer"
    btn.onclick = function (e) { remove_title(id) };
    var txt = document.createTextNode( title );
    li.appendChild(btn);
    li.appendChild(txt);
    panier.appendChild(li);
}

function refresh_search(search) {
    var reslist = document.getElementById("results-list");
    while (reslist.firstChild) {
      reslist.removeChild(reslist.lastChild);
    }
    search.forEach(function (item, index) {
      var title = item['Ttl'];
      var id = item['RscId'];
      var li=document.createElement('li');
      var btn = document.createElement("input");
      btn.type="button";
      btn.value="Ajouter"
      btn.onclick = function (e) { add_title(title,id) };
      var txt = document.createTextNode( title );
      li.appendChild(btn);
      li.appendChild(txt);
      reslist.appendChild(li);
    });
}

function sayHello() {
    searchstr = document.getElementById("search").value;
    searchstr = searchstr.replace(/\s{2,}/g,' ');
    searchstr = searchstr.replace(/\s/g, "-");
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        refresh_search(JSON.parse(this.responseText));
      }
    };
   xhttp.open("GET", "search?q="+searchstr, true);
   xhttp.send();
}

