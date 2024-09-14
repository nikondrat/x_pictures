import 'package:flutter/material.dart';
import 'package:toggle_switch/toggle_switch.dart';
import 'package:x_pictures/src/data.dart';

class SelectModeWidget extends StatelessWidget {
  const SelectModeWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        ToggleSwitch(
          minWidth: 400,
          totalSwitches: 2,
          animate: true,
          animationDuration: 400,
          inactiveBgColor: AppColors.kSecondaryAdditionallyColor,
          radiusStyle: true,
          labels: [
            t.generateView.type.images,
            t.generateView.type.video,
          ],
        ),
      ],
    );

    // return Observer(builder: (context) {
    //   return SizedBox(
    //     height: 30.r,
    //     child: Row(
    //       children: [
    //         Expanded(
    //             child: _Tab(
    //           onTap: () => store.setSelected(0),
    //           title: t.generateView.type.images,
    //           isSelected: store.selected == 0,
    //         )),
    //         Expanded(
    //             child: _Tab(
    //           onTap: () => store.setSelected(1),
    //           title: t.generateView.type.video,
    //           isSelected: store.selected == 1,
    //         )),
    //       ],
    //     ),
    //   );
    // });
  }
}

// class _Tab extends StatelessWidget {
//   final Function() onTap;
//   final String title;
//   final bool isSelected;
//   const _Tab(
//       {required this.onTap, required this.title, required this.isSelected});

//   @override
//   Widget build(BuildContext context) {
//     final ThemeData themeData = Theme.of(context);
//     final TextTheme textTheme = themeData.textTheme;
//     final ColorScheme colorScheme = themeData.colorScheme;

//     return isSelected
//         ? GradientButton(
//             onPressed: onTap,
//             text: title,
//             padding:
//                 const EdgeInsets.symmetric(vertical: AppValues.kPadding / 4),
//             textStyle: textTheme.bodyLarge!.copyWith(
//               fontSize: 14.sp,
//             ),
//           )
//         : Column(
//             crossAxisAlignment: CrossAxisAlignment.stretch,
//             children: [
//               Expanded(
//                 child: TextButton(
//                   onPressed: onTap,
//                   style: const ButtonStyle(
//                       padding: WidgetStatePropertyAll(
//                         EdgeInsets.symmetric(
//                           vertical: AppValues.kPadding / 4,
//                         ),
//                       ),
//                       shape: WidgetStatePropertyAll(RoundedRectangleBorder(
//                           borderRadius: BorderRadius.horizontal(
//                               right: Radius.circular(AppValues.kRadius)))),
//                       backgroundColor: WidgetStatePropertyAll(
//                           AppColors.kSecondaryAdditionallyColor)),
//                   child: AutoSizeText(
//                     title,
//                     style: textTheme.bodyLarge!.copyWith(
//                       color: colorScheme.onSurface,
//                       fontSize: 14.sp,
//                     ),
//                   ),
//                 ),
//               ),
//             ],
//           );
//   }
// }
