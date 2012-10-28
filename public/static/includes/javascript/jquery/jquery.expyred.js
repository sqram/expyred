$(document).ready(function(){

	// Show/hide 'loading' image
	$(".loading").ajaxStart(function(){ $(this).show(); });
	$(".loading").ajaxStop(function(){ $(this).hide(); });

	
	// make odd <td>s bold
	$('table td:nth-child(odd)').addClass('bold')

	// Tooltip for <th>s
	$('th[title]').qtip({
		style: {
			name: 'cream',
			tip: true,			
			title: { 'font-size': 10 },
			width: 300
		},
		adjust: {
			screen: true,
			resize: true
		},
		position: {
			corner: {
				target: 'topMiddle',
				tooltip: 'bottomMiddle'
			}
		}
	})
	
	//$('#regex').copy()
	$('clipboard').click(function() {
		$("#regex").copy()				 
	 });

	
	// If page is loaded with form values populated,
	// then it means its a permalink. Run regex
	if( $('#regex').val() != '' && $('#test_string').val() != '' ) {
		parse_regex()
	}
	
	

	// Hilite options field when options table is hovered
	$('.flags').hover(function() {
		$('#options').addClass('warning')
	},function() {
		$('#options').removeClass('warning')
	});
	
	
	// Auto-grow textarea
	$('textarea').autogrow()
	
	// Allow tabs in textarea
	 $("textarea").tabby();
	
	
	// Call parse_regex() on keypress
	$('#test_string, #regex, #options').livequery('keyup', function(e) {
		// Parse only if both regex and test_string fields have a value
		if( $('#regex').val() != '' && $('#test_string').val() != '' ) {
			special_keys =  [
			16, 17, 18, 27, 145, 20, 144, 19, 45, 36, 35, 33, 34, 37, 38, 39,
			40, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123,
			];
			
			// Don't ajax if key pressed is special(ie: esc, shift, etc)
			if( special_keys.indexOf(e.keyCode) == -1 ) {
				parse_regex()
			}
		}
	});
	
	
	
	// When permalink is clicked
	$('#permalink').click(function() {
		regex = $('#regex').val()
		string = $('#test_string').val()
		options = $('#options').val()
		$.ajax({
			type: "POST",
			url : '/permalink',
			dataType: 'json',
			data: ({ permalink: 'permalink', string: string, regex : regex, options : options  }),
			success: function(msg) {
				if( msg.result == 'success') {
					$('#link_response').removeClass('hidden')
					$('#link_response').addClass('response')
					$('#link_response').html('http://expyred.kat.sh/' + msg.text)
				}
			}
		});
	});
	
	
	
	// Parse the regex
	function parse_regex() { 
		regex = $('#regex').val()
		string = $('#test_string').val()
		options = $('#options').val()
	
		$.ajax({
			type: "POST",
			url : '/',
			dataType: 'json',
			data: ({ string: string, regex : regex, options : options  }),
			success: function(msg) {
				$('#result').removeClass()
				if( msg.result == 'no-match' ) {
					$('#result').addClass('no-matches')
					$('#result').html('No matches found.')
				} else if( msg.result == 'match' ){
					$('#result').addClass('result')
					$('#result').html(msg.string)
				} else if( msg.result == 'failure' ) {
					$('#result').addClass('warning')
					$('#result').html(msg.error)

				}
				
			}
		});
	}
	

}); // End jQuery
