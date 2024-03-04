{%include 'header.html'%}
<div class="container" style="margin:0 auto;padding-top:100px;">
<div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12" >
    <div class="card" >
        <h5 class="card-header">Follow Users</h5>
        <div class="card-body">
            <div class="table-responsive ">
                <table class="table table-bordered">
                    <thead style="background: blue;color: #FFF">
                        <tr class="white">
                            <th>Sno</th>
							<th>Username</th>
							<th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for i in detail %}
                        <tr style="background: #FFF;color: #000">
                       
							<td>{{ i.name }}</td>
							
							<td>
							
							
							<a href="" class="btn btn-success"> Follow </a>
							<a href="" class="btn btn-danger"> UnFollow </a>
							
							</td>
						</tr>
                        {% empty %}
                        <tr>
                            <td colspan="8" class="text-center bg-primary">No Post</td>
                        </tr>
                       {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
</div>
