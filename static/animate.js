panier = new Set();
image_map = {};

function get_panier() {  return Array.from(panier);  }
function refresh_standalone_link() {
  var link = window.location.href.split('?')[0];
  if (panier.size > 0) { link += "?q=" + get_panier().join(","); }
  document.getElementById("standalone").innerHTML=link;
  document.getElementById("standalone").href=link;
}


function get_title(id) { return image_map[id]['Title']; }
function get_link(id) { return image_map[id]['Link']; }
function get_image(id) {
  return 'https://'+image_map[id]['Img']+'/SMALL?fallback=https://bibliotheques.paris.fr/ui/skins/default/portal/front/images/General/DocType/BDTP_SMALL.png';
}


function mklink(title,link) {
  var a = document.createElement('a');
  a.target="_blank"
  a.rel="noopener noreferrer"
  a.title = title;
  a.innerHTML = title;
  a.href  = link;
  return a;
}

function get_sitedir_foot(site) {
  site = site.split(" - ")
  res = "https://www.google.com/maps/dir/?api=1&origin=112+Rue+de+la+Tombe+Issoire,+75014+Paris,+France&destination=Bibliothèque+" + encodeURI(site[1]) + ",+" + encodeURI(site[0]) + "&travelmode=transit"
  return mklink("Go !",res)
}


function get_tick_yes() {
  var node = document.createElement('span');
  node.className = "tickyes"
  node.innerHTML = '&#10004;'
  return node;
}

function get_tick_no() {
  var node = document.createElement('span');
  node.className = "tickno"
  node.innerHTML = '&#10008;'
  return node;
}


function removeAllNodes(nodeid) {
  var node = document.getElementById(nodeid);
  while (node.firstChild) {  node.removeChild(node.lastChild);  }
  return node;
}

function refresh_report(data) {
  var report = removeAllNodes("report");
  var report_sites=data[0];
  var report_holdings=data[1];

  var tr = document.createElement('tr');
  tr.appendChild( document.createElement('td') );
  tr.appendChild( document.createElement('td') );
  get_panier().forEach(function (item, index) {
      var td = document.createElement('td');
      var img = document.createElement('img');
      img.src=get_image(item);
      img.alt = get_title(item);
      img.title = get_title(item);
      img.name = get_title(item);
      td.appendChild(img);
      tr.appendChild(td);
    });
  report.appendChild(tr);

  report_sites.forEach(function (item, index) {
      var id = item['SiteCode'];
      var tr = document.createElement('tr');

      var td = document.createElement('td');
      td.appendChild( mklink(item['Site'], item['Link']) );
      tr.id = id;
      tr.appendChild(td);

      var td = document.createElement('td');
      td.appendChild( get_sitedir_foot(item['Site']) );
      tr.appendChild(td);

      get_panier().forEach(function (item, index) {
        var td = document.createElement('td');
        if (report_holdings[item].indexOf(id) >= 0) {
          td.appendChild( get_tick_yes() );
        } else {
          td.appendChild( get_tick_no() );
        }
        tr.appendChild(td);
      });

      report.appendChild(tr);
    });
}

function generate() {
  document.getElementById("search").value="";
  removeAllNodes("results-list");
  removeAllNodes("report");
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      refresh_report(JSON.parse(this.responseText));
    }
  };
  xhttp.open("GET", "report?q=" + get_panier(), true);
  xhttp.send();
}

function remove_title(id) {
    panier.delete(id);
    refresh_standalone_link();
    var node = document.getElementById("panier");
    node.childNodes.forEach(function (item, index) {
        if (item.id == id) {  node.removeChild(item);  }
    });
}

function add_title(id) {
    if (panier.has(id)) { return; }
    panier.add(id);
    refresh_standalone_link();
    var li=document.createElement('li');
    li.id=id
    li.img=get_image(id)
    var btn = document.createElement("input");
    btn.type="button"
    btn.value="Supprimer"
    btn.onclick = function (e) { remove_title(id) };
    li.appendChild(btn);
    li.appendChild( mklink( get_title(id), get_link(id) ) );
    document.getElementById("panier").appendChild(li);
}

function refresh_search(search) {
    var reslist = removeAllNodes("results-list");
    search = search.sort( function (a,b) { return a.Title.localeCompare(b.Title); } );
    search.forEach(function (item, index) {
      var id = item['RscId'];
      image_map[id] = item;
      var li=document.createElement('li');
      var btn = document.createElement("input");
      btn.type="button";
      btn.value="Ajouter"
      btn.onclick = function (e) { add_title(id) };
      li.appendChild(btn);
      li.appendChild(mklink(get_title(id), get_link(id)));
      reslist.appendChild(li);
    });
}

function search() {
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

function add_image_map(ids) {
   ids.forEach(function (item, index) {
       var id = item['RscId'];
       image_map[id] = item;
       add_title(id);
     });
   generate();
}

if (window.location.href.split('?q=').length > 1) {
  params = window.location.href.split('?q=')[1].split(',');
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        add_image_map(JSON.parse(this.responseText));
      }
    };
   xhttp.open("GET", "ids?q="+params, true);
   xhttp.send();
}


