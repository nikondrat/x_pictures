import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

// class SearchBarWidget extends StatelessWidget {
//   const SearchBarWidget({super.key});

//   @override
//   Widget build(BuildContext context) {
//     final ThemeData themeData = Theme.of(context);
//     final TextTheme textTheme = themeData.textTheme;
//     final ColorScheme scheme = themeData.colorScheme;

//     return TextField(
//       decoration: InputDecoration(
//         icon: Icon(Icons.search, color: scheme.secondary),
//         hintText: t.homeView.search,
//         hintStyle: textTheme.bodyLarge!.copyWith(color: scheme.secondary),
//         enabledBorder: OutlineInputBorder(
//           borderRadius: BorderRadius.circular(AppValues.kRadius),
//           borderSide: BorderSide.none,
//         ),
//         focusedBorder: OutlineInputBorder(
//             borderSide: BorderSide.none,
//             borderRadius: BorderRadius.circular(AppValues.kRadius)),
//         fillColor: AppColors.kSecondaryAdditionallyColor,
//         focusColor: AppColors.kSearchBarActiveColor,
//         // hoverColor: AppColors.kSecondaryAdditionallyColor,
//         // fillColor: AppColors.kSecondaryAdditionallyColor
//       ),
//     );
//   }
// }

class SearchBarWidget extends StatefulWidget {
  final PacksStore store;
  const SearchBarWidget({
    super.key,
    required this.store,
  });

  @override
  _SearchBarWidgetState createState() => _SearchBarWidgetState();
}

class _SearchBarWidgetState extends State<SearchBarWidget> {
  late FocusNode _focusNode;
  bool _hasFocus = false;

  late final TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
    _focusNode = FocusNode();
    _focusNode.addListener(() {
      setState(() {
        _hasFocus = _focusNode.hasFocus;
      });
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    _focusNode.dispose();
    super.dispose();
  }

  void _clearTextField() {
    setState(() {
      _hasFocus = false;
    });
    _controller.clear();
    widget.store.setQuery('');

    _focusNode.unfocus();
  }

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme scheme = themeData.colorScheme;

    return Row(
      children: [
        Expanded(
          child: TextField(
            controller: _controller,
            focusNode: _focusNode,
            onChanged: (value) {
              widget.store.setQuery(value);
            },
            decoration: InputDecoration(
              prefixIcon: Icon(Icons.search, color: scheme.secondary),
              suffixIcon: Icon(Icons.keyboard_voice, color: scheme.secondary),
              hintText: t.homeView.search,
              hintStyle: textTheme.bodyLarge!.copyWith(color: scheme.outline),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(AppValues.kRadius),
                borderSide: BorderSide.none,
              ),
              focusedBorder: OutlineInputBorder(
                  borderSide: BorderSide.none,
                  borderRadius: BorderRadius.circular(AppValues.kRadius)),
              fillColor: AppColors.kSecondaryAdditionallyColor,
              focusColor: AppColors.kSecondaryAdditionallyColor,
              hoverColor: AppColors.kSecondaryAdditionallyColor,
            ),
          ),
        ),
        if (_hasFocus)
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: AppValues.kPadding),
            child: GestureDetector(
                onTap: _clearTextField,
                child: AutoSizeText(
                  t.common.cancel,
                  style: textTheme.bodyLarge,
                )),
          )
      ],
    );

    // return Container(
    //   padding: EdgeInsets.symmetric(horizontal: 16),
    //   decoration: BoxDecoration(
    //     color: _hasFocus ? Colors.grey[300] : Colors.white,
    //     border: Border.all(color: Colors.grey),
    //     borderRadius: BorderRadius.circular(8),
    //   ),
    //   child: Row(
    //     children: [
    //       Expanded(
    //         child: TextField(
    //           focusNode: _focusNode,
    //           decoration: InputDecoration(
    //             hintText: 'Введите текст...',
    //             border: InputBorder.none,
    //           ),
    //         ),
    //       ),
    //       if (_hasFocus)
    //         IconButton(
    //           icon: Icon(Icons.cancel),
    //           onPressed: _clearTextField,
    //         ),
    //     ],
    //   ),
    // );
  }
}
