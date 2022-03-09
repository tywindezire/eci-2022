
function csvMake(url,id,name){
  $.ajax({
   url:url,
   dataType:"text",
   success:function(data)
   {
    var row = data.split(/\r?\n|\r/);
     var table_data = '<table class="table striped" id="'+name+'"><thead><th ">Constituency Name</th>  <th> Leading party candidate</th> <th>Leading party</th><th> Trailing party candidate</th>  <th> Trailing party</th><th data-sortas="numeric">Margin</th> <th> Result</th></thead>';
    for(var count = 0; count<row.length; count++)
    {
     var cell_data = row[count].split(",");
     table_data += '<tr>';
     for(var cell_count=0; cell_count<cell_data.length; cell_count++)
     {
      
       table_data += '<td>'+cell_data[cell_count]+'</td>';
      
     }
     table_data += '</tr>';
    }
    table_data += '</table>';
    $('#'+id).append(table_data);
    
    $("#"+name).fancyTable({
			pagination: true,
			perPage:15,
      sortColumn: 6,
			globalSearch:true
		});	
    table_data='';
   }
   
  });
}
$(document).ready(function(){
  
  $.get(csvl, function( data ) {
    data=data.split('\n');
    for(var i =0;i<data.length;i++)
    {
      csvMake(data[i].split(',')[1],"table"+i,data[i].split(',')[0]);
      
     
      $('.tabs').append('<li class="tab " style=""><a href="#'+"table"+i+'"><b>'+data[i].split(',')[0]+'</b></a></li>');
      

    }
    
    $('.tabs').tabs();
    $('.progress').fadeOut('slow');
  
});

 });
 