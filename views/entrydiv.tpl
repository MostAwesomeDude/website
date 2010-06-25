%import datetime

%import bottle

%url = "/entry/%s" % name

<h2 class="title">
%if bottle.request.fullpath != url:
<a href="/entry/{{name}}">{{headline}}</a>
%else:
{{headline}}
%end
</h2>
<div class="content">
%for paragraph in paragraphs:
<p>{{!paragraph}}</p>
%end
<p>~ C.</p>
<p>Created on {{datetime.datetime.fromtimestamp(ctime).strftime("%b %d, %Y")}}</p>
%if mtime != ctime:
<p>Last modified on {{datetime.datetime.fromtimestamp(mtime).strftime("%b %d, %Y")}}</p>
%end
</div>
