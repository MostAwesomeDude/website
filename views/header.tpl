%import bottle

%home = "/"

<div id="header" class="clear-block">
  <div class="header-right">
    <div class="header-left">

      <div id="logo-title">
%if bottle.request.fullpath != home:
<a href={{home}} title="Home"><img src= "/static/matrix-keys.png" alt="Home"
id="logo" name="logo" /></a>
%else:
<img src= "/static/matrix-keys.png" alt="Home" id="logo" name="logo" />
%end
      </div><!-- /logo-title -->

      <div id="name-and-slogan">
%if bottle.request.fullpath != home:
<h1 id='site-name'><a href={{home}} title="Home">Corbin Simpson</a></h1>
%else:
<h1 id='site-name'>Corbin Simpson</h1>
%end
        <div id='site-slogan'>
          Most awesome, dude!
        </div>
      </div><!-- /name-and-slogan -->
    </div><!-- /header-left -->
  </div><!-- /header-right -->
</div><!-- /header -->
