import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class _Format {
  final double width;
  final double height;
  _Format({required this.width, required this.height});
}

class GenerateFormats extends StatelessWidget {
  final double windowHeight;
  const GenerateFormats({super.key, required this.windowHeight});

  @override
  Widget build(BuildContext context) {
    final List<_Format> formats = [
      _Format(width: 2, height: 3),
      _Format(width: 3, height: 2),
      _Format(width: 1, height: 1),
      _Format(width: 19, height: 6),
      _Format(width: 16, height: 9),
    ];

    return TitleWithBody(
      title: t.generateView.format,
      action: const ResetButton(),
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Row(
          children: formats
              .map((e) => _FormatWidget(
                    format: e,
                    windowHeight: windowHeight,
                  ))
              .toList(),
        ),
      ),
    );
  }
}

class _FormatWidget extends StatelessWidget {
  final _Format format;
  final double windowHeight;

  const _FormatWidget({
    required this.format,
    required this.windowHeight,
  });

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    final double fixedWidth = windowHeight * .06;
    final double height = fixedWidth * (format.height / format.width);

    return Padding(
      padding: const EdgeInsets.all(AppValues.kPadding / 4),
      child: SizedBox(
        width: fixedWidth,
        height: height,
        child: Container(
          decoration: BoxDecoration(
            border: Border.all(color: AppColors.kOutlineColor),
            borderRadius: BorderRadius.circular(AppValues.kPadding / 2),
          ),
          child: Center(
            child: AutoSizeText(
                '${format.width.toInt()}:${format.height.toInt()}',
                style: textTheme.bodyLarge!.copyWith(
                    color: colorScheme.secondary, fontWeight: FontWeight.bold)),
          ),
        ),
      ),
    );
  }
}
