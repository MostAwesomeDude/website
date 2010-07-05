%url = "/"

%include head title=title

<body>
<div id="body">
%include header

  <div id="main">
%for album, songs in albums.iteritems():
    <h2>{{"%s (%s)" % album}}</h2>
    <ul>
%for song in songs:
      <li>{{!'<a href="/%s">%s</a>' % song[0:2]}}</li>
%end
    </ul>
%end
  </div>

%include footer preptime=time
</div>
</body>
</html>
