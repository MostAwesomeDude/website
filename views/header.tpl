%import bottle

%home = "/"

<div id="header">
  <div id="header-left">
%if bottle.request.fullpath != home:
<a href={{home}} title="Home"><img src= "/static/matrix-keys.png" alt="Home"
id="logo" name="logo" /></a>
%else:
<img src= "/static/matrix-keys.png" alt="Home" id="logo" name="logo" />
%end
  </div>

  <div id="header-right">
  Right-hand placeholder
  </div>

  <div id="header-center">
%if bottle.request.fullpath != home:
<h1 id='site-name'><a href={{home}} title="Home">Corbin Simpson</a></h1>
%else:
<h1 id='site-name'>Corbin Simpson</h1>
%end
  Most awesome, dude!
  </div>
</div>
