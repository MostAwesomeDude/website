%url = "/"

%include head title=title

<body>
<div id="body">
%include header

  <div id="main">
%for entry in entries:
  %include entrydiv **entry
%end
  </div>

%include footer preptime=time
</div>

%include valid

<!--
To view, :s/\~/-/g
~~~~~BEGIN GEEK CODE BLOCK~~~~~
Version: 3.1
GMU/CS/CM d s+:++ a~~ C+++++ L++++ Py+++$ E~~~ W+++ !N w~ M~~ PS++ PE~ Y+
PGP+ t+ X~ R* !tv b+++ DI+ G e* r++ r++ y+++**?
~~~~~~END GEEK CODE BLOCK~~~~~~
-->
</body>
</html>
