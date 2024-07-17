import 'package:flutter/widgets.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class GenerateBody extends StatefulWidget {
  final GenerateStore store;
  final double windowHeight;
  const GenerateBody(
      {super.key, required this.store, required this.windowHeight});

  @override
  State<GenerateBody> createState() => _GenerateBodyState();
}

class _GenerateBodyState extends State<GenerateBody> {
  @override
  void initState() {
    widget.store.fetchFilter();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const Gap(AppValues.kPadding),
        const SelectModeWidget(),
        const Gap(AppValues.kPadding),
        const GenerateStyles(),
        const Gap(AppValues.kPadding),
        const GenerateTags(),
        const Gap(AppValues.kPadding),
        GenerateFormats(
          windowHeight: widget.windowHeight,
        ),
        const Gap(AppValues.kPadding),
        const AddDescription(),
        const Gap(AppValues.kPadding),
      ],
    );
  }
}
