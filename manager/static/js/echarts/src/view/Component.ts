/*
* Licensed to the Apache Software Foundation (ASF) under one
* or more contributor license agreements.  See the NOTICE file
* distributed with this work for additional information
* regarding copyright ownership.  The ASF licenses this file
* to you under the Apache License, Version 2.0 (the
* "License"); you may not use this file except in compliance
* with the License.  You may obtain a copy of the License at
*
*   http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing,
* software distributed under the License is distributed on an
* "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
* KIND, either express or implied.  See the License for the
* specific language governing permissions and limitations
* under the License.
*/

import Group from 'zrender/src/graphic/Group';
import * as componentUtil from '../util/component';
import * as clazzUtil from '../util/clazz';
import ComponentModel from '../model/Component';
import GlobalModel from '../model/Global';
import ExtensionAPI from '../core/ExtensionAPI';
import {Payload, ViewRootGroup, ECActionEvent, EventQueryItem, ECElementEvent} from '../util/types';
import Element from 'zrender/src/Element';
import SeriesModel from '../model/Series';

interface ComponentView {
    /**
     * Implement it if needed.
     */
    updateTransform?(
        model: ComponentModel, ecModel: GlobalModel, api: ExtensionAPI, payload: Payload
    ): void | {update: true};

    /**
     * Pass only when return `true`.
     * Implement it if needed.
     */
    filterForExposedEvent(
        eventType: string, query: EventQueryItem, targetEl: Element, packedEvent: ECActionEvent | ECElementEvent
    ): boolean;

    /**
     * Find dispatchers for highlight/downplay by name.
     * If this methods provided, hover link (within the same name) is enabled in component.
     * That is, in component, a name can correspond to multiple dispatchers.
     * Those dispatchers can have no common ancestor.
     * The highlight/downplay state change will be applied on the
     * dispatchers and their descendents.
     *
     * @return Must return an array but not null/undefined.
     */
    findHighDownDispatchers?(
        name: string
    ): Element[];

    focusBlurEnabled?: boolean;
}

class ComponentView {

    // [Caution]: Because this class or desecendants can be used as `XXX.extend(subProto)`,
    // the class members must not be initialized in constructor or declaration place.
    // Otherwise there is bad case:
    //   class A {xxx = 1;}
    //   enableClassExtend(A);
    //   class B extends A {}
    //   var C = B.extend({xxx: 5});
    //   var c = new C();
    //   console.log(c.xxx); // expect 5 but always 1.

    readonly group: ViewRootGroup;

    readonly uid: string;

    // ----------------------
    // Injectable properties
    // ----------------------
    __model: ComponentModel;
    __alive: boolean;
    __id: string;

    constructor() {
        this.group = new Group();
        this.uid = componentUtil.getUID('viewComponent');
    }

    init(ecModel: GlobalModel, api: ExtensionAPI): void {}

    render(model: ComponentModel, ecModel: GlobalModel, api: ExtensionAPI, payload: Payload): void {}

    dispose(ecModel: GlobalModel, api: ExtensionAPI): void {}

    updateView(model: ComponentModel, ecModel: GlobalModel, api: ExtensionAPI, payload: Payload): void {
        // Do nothing;
    }

    updateLayout(model: ComponentModel, ecModel: GlobalModel, api: ExtensionAPI, payload: Payload): void {
        // Do nothing;
    }

    updateVisual(model: ComponentModel, ecModel: GlobalModel, api: ExtensionAPI, payload: Payload): void {
        // Do nothing;
    }

    /**
     * Hook for toggle blur target series.
     * Can be used in marker for blur or leave blur the markers
     */
    toggleBlurSeries(seriesModels: SeriesModel[], isBlur: boolean, ecModel: GlobalModel): void {
        // Do nothing;
    }

    /**
     * Traverse the new rendered elements.
     *
     * It will traverse the new added element in progressive rendering.
     * And traverse all in normal rendering.
     */
    eachRendered(cb: (el: Element) => boolean | void) {
        const group = this.group;
        if (group) {
            group.traverse(cb);
        }
    }

    static registerClass: clazzUtil.ClassManager['registerClass'];
};


export type ComponentViewConstructor = typeof ComponentView
    & clazzUtil.ExtendableConstructor
    & clazzUtil.ClassManager;

clazzUtil.enableClassExtend(ComponentView as ComponentViewConstructor);
clazzUtil.enableClassManagement(ComponentView as ComponentViewConstructor);

export default ComponentView;
