frappe.ui.form.on('AI Assistant', {
    refresh: function(frm) {
        // Make the chatbox read-only
        frm.set_df_property('chatbox', 'read_only', 1);

        // Add a keypress event listener to the message input to handle the Enter key
        $(frm.fields_dict.message.input).on('keypress', function(e) {
            if (e.which === 13 && !e.shiftKey) { // Check if Enter key is pressed without Shift
                e.preventDefault();  // Prevent the default form submission
                send_message(frm);
            }
        });
    },
    send: function(frm) {  // Triggered by the 'send' button
        send_message(frm);
    }
});

function send_message(frm) {
    // Check if message field is not empty
    var message = frm.doc.message.trim();
    if (message) {
        frm.call({
            method: "send_message",
            doc: frm.doc,
            callback: function(r) {
                if (!r.exc) {
                    // Update the 'chatbox' field with the response from the server.
                    frm.set_value('chatbox', r.message);
                    frm.refresh_field('chatbox');
                    frm.set_value('message', ''); // Clear the message field after sending
                    frm.refresh_field('message');
                } else {
                    // Handle any exceptions or errors
                    frappe.msgprint({
                        title: __('Error'),
                        indicator: 'red',
                        message: __('Failed to get a response. Please try again.')
                    });
                }
            }
        });
    } else {
        frappe.msgprint(__('Please enter a message before sending.'));
    }
}

