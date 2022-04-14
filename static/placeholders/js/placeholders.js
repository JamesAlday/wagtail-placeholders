const React = window.React;
const Modifier = window.DraftJS.Modifier;
const EditorState = window.DraftJS.EditorState;

class PlaceholderSource extends React.Component {
  constructor(props) {
    super(props);
    this.onClose = this.onClose.bind(this);
  }

  componentDidMount() {
    const { editorState, entityType, onComplete } = this.props;
    const content = editorState.getCurrentContent();
    const selection = editorState.getSelection();
    const activePage = $('.menu-active').text().trim().toLowerCase()
    
    let modalUrl = "/placeholders/"
    let modalData = {}

    if (activePage == 'alerts') {
      modalData['page'] = activePage
      modalData['filter'] = 'type__id'
      modalData['filter_value'] = $('#id_type option:selected').val()

      if (modalData['filter_value'] == '') {
        alert("Placeholders are using default values. Select an Alert Type to see type-specific placeholders.")
      }
    }

    $(document.body).on("hidden.bs.modal", this.onClose);

    $("body > .modal").remove();

    $.ajax({
      type: "get",
      url: modalUrl,
      data: modalData,
      dataType: "html",
      success: function (data) {
        $("body").append(data);

        var placeholders = $("#placeholders-listing tbody tr");

        placeholders.each(function (idx, row) {
          row.addEventListener('click', function() {
            const placeholderTag = event.target.parentElement.dataset["tag"];

            // Uses the Draft.js API to create a new entity with the right data.
            const contentWithEntity = content.createEntity(
              entityType.type,
              "IMMUTABLE",
              {
                placeholder: placeholderTag,
              }
            );
            const entityKey = contentWithEntity.getLastCreatedEntityKey();

            // We also add some text for the entity to be activated on.
            const text = `{{${placeholderTag}}}`;

            const newContent = Modifier.replaceText(
              content,
              selection,
              text,
              null,
              entityKey
            );
            const nextState = EditorState.push(
              editorState,
              newContent,
              "insert-characters"
            );

            onComplete(nextState);

            // Create a hidden list item on the page to save the reference
            var item = $("<li id='placeholder-" + idx + "'>" + placeholderTag + "</li>");
            $("#placeholders ol").append(item)

            $("#placeholders-modal").modal("hide");
          }, false);
        });

        $("#placeholders-modal").modal("show");
      }
    });
  }

  onClose(e) {
    const { onClose } = this.props;
    e.preventDefault();
    onClose();
  }

  render() {
    return null;
  }
}

const Placeholder = (props) => {
  const { entityKey, contentState } = props;
  const data = contentState.getEntity(entityKey).getData();
  props.className = "placeholder-tag"
  return React.createElement("span", props, props.children);
};

window.draftail.registerPlugin({
  type: "PLACEHOLDERS",
  source: PlaceholderSource,
  decorator: Placeholder,
});