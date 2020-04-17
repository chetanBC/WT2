returnObj = {
    show:function()
    {
    	this.xhr =new XMLHttpRequest();
    	temp = this;
    	var input = document.getElementById('search').value;
    	console.log(input);
    	var term =""

        if(input == "Dell Inspiron")
        {
            term="EL1";
        }
        else if(input == "Apple MacBook Pro")
        {
            term="EL2";
        }
        else if(input == 'Lenovo Ideapad')
        {
            term="EL3";
        }
        else if(input == "HP Spectre x360")
        {
            term="EL4";
        }
        else if(input == "Acer Predator Helios 300")
        {
            term="EL5";
        }
        else if(input == "Apple iPhone 8 Plus")
        {
            term="EM1";
        }
        else if(input == "Samsung Galaxy S20")
        {
            term="EM2";
        }
        else if(input == "Redmi 8")
        {
            term="EM3";
        }
        else if(input == "Honor 20i")
        {
            term="EM4";
        }
        else if(input == "Asus ZenFone Max M2")
        {
            term="EM5";
        }
        else if(input == "LG LED Smart TV")
        {
            term="TT1";
        }
        else if(input == "Samsung LED Smart TV")
        {
            term="TT2";
        }
        else if(input == "Mi LED Smart TV")
        {
            term="TT3";
        }
        else if(input == "Sony Bravia R202F LED TV")
        {
            term="TT4";
        }
        else if(input == "Motorola LED Smart TV")
        {
            term="TT5";
        }
        else if(input == "Samsung 6 kg washmachine")
        {
            term="TW1";
        }
        else if(input == "IFB 8 kg washmachine")
        {
            term="TW2";
        }
        else if(input == "LG 8 kg washmachine")
        {
            term="TW3";
        }
        else if(input == "Bosch 7 kg washmachine")
        {
            term="TW4";
        }
        else if(input == "Whirlpool 6.5 kg washmachine")
        {
            term="TW5";
        }
       
    	this.xhr.onreadystatechange = this.display;
    	this.xhr.open("GET","http://127.0.0.1:5000/api/getitemdata/"+term,true);
      	this.xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
      	this.xhr.send();
     },

     display:function()
     {
     	
     	if(this.readyState == 4 && this.status == 200){
     		var item = document.getElementById('item');
	        var hide = document.getElementById('hide');
	        item.style.display = "block"
	        hide.style.display = "none"

            var json = JSON.parse(this.responseText);
	        var itemid = document.getElementById('itemid');
	        var name = document.getElementById('name');
	        var image = document.getElementById('img');
	        var price = document.getElementById('price');
            var specs = document.getElementById('specs');
            var quant = document.getElementById('quant');
            image.src = "./images/" + json[0][0] + ".jpeg"
            itemid.innerHTML= json[0][0]
	        name.innerHTML = json[0][1];
            price.innerHTML = json[0][2];
            specs.innerHTML = json[0][3];
            quant.innerHTML = "Quantity :" + json[0][4];

        
    	}
    },
    setCookieFunction:function(setval)
    {
          document.cookie = "Page="+setval;
    }
}
function Suggest(){
    this.xhr = new XMLHttpRequest();
    tempObj = this;
    this.search = null;
    this.timer = null
    this.getTerm = function()
    {   
        console.log('in');
          var dd = document.getElementById("dd");
          dd.innerHTML = "";
          if(tempObj.timer)
          {
              clearTimeout(tempObj.timer)
          }
          this.timer = setTimeout(tempObj.sendTerm,500);                    
    }
    
    
    this.sendTerm = function()
    {
          tempObj.xhr.onreadystatechange = tempObj.displayResults;
          tempObj.search = document.getElementById("search");
          // tempObj.xhr.open("GET","subthrot.php?term="+tempObj.search.value,true);
          var term = tempObj.search.value;
          if(term == '')
              term = -1;
          //tempObj.xhr.open("GET","subthrot.php?term="+tempObj.search.value,true);
          tempObj.xhr.open("GET","http://127.0.0.1:5000/api/search/"+term,true);
          tempObj.xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
          tempObj.xhr.send();
    }
    

    this.displayResults = function()
    {
          if(this.readyState == 4 && this.status == 200){
              var json = JSON.parse(this.responseText);
              tempObj.search.style.backgroundColor = "white";
              if(json.length == 0)
              {
                  //tempObj.search.value = "No results found"
                  tempObj.search.style.backgroundColor = "red";
                  if(tempObj.search.value == '')
                      tempObj.search.style.backgroundColor = "white";
              }
              else{
                  tempObj.populateFood(json);
              }

          }
    }
    this.populateFood = function(items)
    {
        var dd = document.getElementById("dd");
        dd.innerHTML = "";
        var dt = document.getElementById("dt");
        for(var i=0;i<items.length;i++)
        {
            var option = document.createElement('option');
            option.value = items[i];
            dd.appendChild(option);
        }
    }


}
var obj = new Suggest();
