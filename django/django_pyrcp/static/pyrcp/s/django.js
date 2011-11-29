/**
 * namespace and basic
 * --------------------
 */
(function($){
    window.pyrcp = {}

    pyrcp.j_doc = $(document);
    
    var csrf_token = '';
    pyrcp.get_csrf = function(){
        if('' === csrf_token){
            csrf_token = $('[name=csrfmiddlewaretoken]').val();
        }
        return csrf_token;
    };
    
    pyrcp.post = function(url, params){
        if('undefined' === typeof params){
            params = {}
        }
        params.type = 'POST';
        
        if('undefined' === typeof params.data){
            params.data = {}
        }
        params.data.csrfmiddlewaretoken = pyrcp.get_csrf();
        
        return $.ajax(url, params);
    };
})(jQuery);