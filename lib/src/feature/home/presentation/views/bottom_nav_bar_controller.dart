import 'dart:ui';

import 'package:auto_size_text/auto_size_text.dart';
import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:provider/provider.dart';
import 'package:svg_flutter/svg.dart';
import 'package:x_pictures/src/data.dart';

class BottomNavBarControllerPage extends StatefulWidget {
  const BottomNavBarControllerPage({super.key});

  @override
  State<BottomNavBarControllerPage> createState() =>
      _BottomNavBarControllerPageState();
}

class _BottomNavBarControllerPageState
    extends State<BottomNavBarControllerPage> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    final List<Widget> pages = [
      const HomeView(),
      const GenerateView(),
      ProfileView(
        goHome: () {
          setState(() {
            _selectedIndex = 0;
          });
        },
        goGenerate: () {
          setState(() {
            _selectedIndex = 1;
          });
        },
        selectedIndex: _selectedIndex,
      )
    ];
    final HomeStore store = context.read();

    return Scaffold(
        resizeToAvoidBottomInset: false,
        backgroundColor: Colors.transparent,
        // bottomNavigationBar: Observer(builder: (context) {
        //   if (!store.showBottomBar) {
        //     return const BottomBarPhotosFuncs();
        //   }

        //   return ClipRRect(
        //     borderRadius: BorderRadius.vertical(top: Radius.circular(20.r)),
        //     child: DecoratedBox(
        //       // decoration: BoxDecoration(),
        //       decoration: BoxDecoration(
        //           border: const Border(
        //               top: BorderSide(
        //             color: Color(0xFF3B3B5A),
        //           )),
        //           borderRadius: BorderRadius.only(
        //             topLeft: Radius.circular(20.r),
        //             topRight: Radius.circular(20.r),
        //           ),
        //           color: const Color(0xff0D1120)),
        //       child: Row(
        //         children: [
        //           BottomNavigationBarItem(
        //             icon: SvgPicture.asset(
        //               Assets.icons.home,
        //               color: _selectedIndex == 0
        //                   ? Colors.orange[900]
        //                   : const Color(0xff6F6F72),
        //               width: 22.h,
        //               height: 22.h,
        //             ),
        //             label: 'Home',
        //           ),
        //           BottomNavigationBarItem(
        //             icon: SvgPicture.asset(
        //               AppIcons.generateIcon,
        //               color: _selectedIndex == 1
        //                   ? Colors.orange[900]
        //                   : const Color(0xff6F6F72),
        //               width: 24.h,
        //               height: 24.h,
        //             ),
        //             label: 'Generate',
        //           ),
        //           BottomNavigationBarItem(
        //             icon: Icon(
        //               Icons.account_circle_outlined,
        //               color: _selectedIndex == 2
        //                   ? Colors.orange[900]
        //                   : const Color(0xff6F6F72),
        //               size: 24.h,
        //             ),
        //             label: 'My Profile',
        //           ),
        //         ].mapIndexed((i, e) {
        //           return Expanded(
        //               child: GestureDetector(
        //             onTap: () {
        //               setState(() {
        //                 _selectedIndex = i;
        //               });
        //             },
        //             child: Padding(
        //               padding: const EdgeInsets.symmetric(
        //                   vertical: AppValues.kPadding / 2),
        //               child: Column(
        //                 mainAxisSize: MainAxisSize.min,
        //                 children: [
        //                   e.icon,
        //                   AutoSizeText(
        //                     e.label!,
        //                     style: TextStyle(
        //                       fontSize: 8.sp,
        //                       fontWeight: _selectedIndex == i
        //                           ? FontWeight.w700
        //                           : FontWeight.w400,
        //                     ),
        //                   ),
        //                 ],
        //               ),
        //             ),
        //           ));
        //         }).toList(),
        //       ),
        //     ),
        //   );

        //   // return ClipRRect(
        //   //   borderRadius: BorderRadius.only(
        //   //     topLeft: Radius.circular(20.r),
        //   //     topRight: Radius.circular(20.r),
        //   //   ),
        //   //   child: BottomNavigationBar(
        //   //     currentIndex: _selectedIndex,
        //   //     onTap: (index) {
        //   //       setState(() {
        //   //         _selectedIndex = index;
        //   //       });
        //   //     },
        //   //     backgroundColor: const Color(0xff0D1120),
        //   //     selectedItemColor: Colors.orange[900],
        //   //     selectedLabelStyle: TextStyle(
        //   //       fontSize: 8.sp,
        //   //       fontWeight: FontWeight.w700,
        //   //     ),
        //   //     selectedIconTheme: IconThemeData(
        //   //       color: Colors.orange[900],
        //   //     ),
        //   //     unselectedIconTheme: const IconThemeData(
        //   //       color: Color(0xff6F6F72),
        //   //     ),
        //   //     unselectedLabelStyle: TextStyle(
        //   //       fontSize: 8.sp,
        //   //       fontWeight: FontWeight.w400,
        //   //       color: const Color(0xff6F6F72),
        //   //     ),
        //   //     unselectedItemColor: const Color(0xff6F6F72),
        //   //     // iconSize: 40,
        //   //     items: [
        //   //       BottomNavigationBarItem(
        //   //         icon: SvgPicture.asset(
        //   //           Assets.icons.home,
        //   //           color: _selectedIndex == 0
        //   //               ? Colors.orange[900]
        //   //               : const Color(0xff6F6F72),
        //   //           width: 22.h,
        //   //           height: 22.h,
        //   //         ),
        //   //         label: 'Home',
        //   //       ),
        //   //       BottomNavigationBarItem(
        //   //         icon: SvgPicture.asset(
        //   //           AppIcons.generateIcon,
        //   //           color: _selectedIndex == 1
        //   //               ? Colors.orange[900]
        //   //               : const Color(0xff6F6F72),
        //   //           width: 24.h,
        //   //           height: 24.h,
        //   //         ),
        //   //         label: 'Generate',
        //   //       ),
        //   //       BottomNavigationBarItem(
        //   //         icon: Icon(
        //   //           Icons.account_circle_outlined,
        //   //           color: _selectedIndex == 2
        //   //               ? Colors.orange[900]
        //   //               : const Color(0xff6F6F72),
        //   //           size: 24.h,
        //   //         ),
        //   //         label: 'My Profile',
        //   //       ),
        //   //     ],
        //   //   ),
        //   // );
        // }),
        body: Stack(alignment: Alignment.bottomCenter, children: [
          pages[_selectedIndex],
          Observer(builder: (context) {
            if (!store.showBottomBar) {
              return const BottomBarPhotosFuncs();
            }

            return BottomBarDecoration(
                child: Row(
              children: [
                BottomNavigationBarItem(
                  icon: SvgPicture.asset(
                    Assets.icons.home,
                    color: _selectedIndex == 0
                        ? Colors.orange[900]
                        : const Color(0xff6F6F72),
                    width: 22.h,
                    height: 22.h,
                  ),
                  label: 'Home',
                ),
                BottomNavigationBarItem(
                  icon: SvgPicture.asset(
                    // AppIcons.generateIcon,
                    Assets.icons.generate,
                    color: _selectedIndex == 1
                        ? Colors.orange[900]
                        : const Color(0xff6F6F72),
                    width: 24.h,
                    height: 24.h,
                  ),
                  label: 'Generate',
                ),
                BottomNavigationBarItem(
                  icon: Icon(
                    Icons.account_circle_outlined,
                    color: _selectedIndex == 2
                        ? Colors.orange[900]
                        : const Color(0xff6F6F72),
                    size: 24.h,
                  ),
                  label: 'My Profile',
                ),
              ].mapIndexed((i, e) {
                return Expanded(
                    child: GestureDetector(
                  onTap: () {
                    setState(() {
                      _selectedIndex = i;
                    });
                  },
                  child: Padding(
                    padding: const EdgeInsets.symmetric(
                        vertical: AppValues.kPadding / 2),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        e.icon,
                        AutoSizeText(
                          e.label!,
                          style: TextStyle(
                            fontSize: 8.sp,
                            fontWeight: _selectedIndex == i
                                ? FontWeight.w700
                                : FontWeight.w400,
                          ),
                        ),
                      ],
                    ),
                  ),
                ));
              }).toList(),
            ));
          }),
        ]));
  }
}
