%import bottle

%home = "/"
%music = "/music"

<div id="header">
  <div id="header-left">
    <img src= "/static/matrix-keys.png" alt="Home" id="logo" name="logo" />
  </div>

  <div id="header-right">
    <a href="http://www.ohloh.net/accounts/34038?ref=Detailed"
    target="_blank"><img style="border:none;" height="35" width="191" src=
    "http://www.ohloh.net/accounts/34038/widgets/account_detailed.gif"
    alt="View ohloh profile" title="View ohloh profile"></a>
    <ul>
%if bottle.request.fullpath != music:
      <li><a href="{{music}}">Music</a></li>
%else:
      <li>Music</li>
%end
    </ul>
  </div>

  <div id="header-center">
%if bottle.request.fullpath != home:
<h1 id='site-name'><a href="{{home}}" title="Home">Corbin Simpson</a></h1>
%else:
<h1 id='site-name'>Corbin Simpson</h1>
%end
  Most awesome, dude!
  </div>
</div>
